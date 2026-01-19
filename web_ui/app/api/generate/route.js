import { NextResponse } from 'next/server'
import { v4 as uuidv4 } from 'uuid'
import path from 'path'
import fs from 'fs/promises'
import { exec } from 'child_process'
import { promisify } from 'util'

const execAsync = promisify(exec)

// Storage for temporary projects
const TEMP_DIR = path.join(process.cwd(), 'temp', 'projects')
const TASKS_FILE = path.join(TEMP_DIR, 'tasks.json')

// Ensure temp directory exists
async function ensureTempDir() {
  try {
    await fs.mkdir(TEMP_DIR, { recursive: true })
  } catch (error) {
    console.error('Failed to create temp directory:', error)
  }
}

// Task storage functions
async function loadTasks() {
  try {
    const data = await fs.readFile(TASKS_FILE, 'utf8')
    return new Map(JSON.parse(data))
  } catch (error) {
    return new Map()
  }
}

async function saveTasks(tasks) {
  try {
    const data = JSON.stringify(Array.from(tasks.entries()))
    await fs.writeFile(TASKS_FILE, data, 'utf8')
  } catch (error) {
    console.error('Failed to save tasks:', error)
  }
}

export async function GET() {
  return NextResponse.json({
    message: "MLOps Project Generator API",
    version: "1.0.0"
  })
}

export async function POST(request) {
  try {
    await ensureTempDir()
    
    const config = await request.json()
    
    // Validate configuration
    const requiredFields = ['framework', 'task_type', 'experiment_tracking', 'orchestration', 'deployment', 'monitoring', 'project_name', 'author_name', 'description']
    const missingFields = requiredFields.filter(field => !config[field])
    
    if (missingFields.length > 0) {
      return NextResponse.json(
        { detail: `Missing required fields: ${missingFields.join(', ')}` },
        { status: 400 }
      )
    }
    
    // Generate unique task ID
    const taskId = uuidv4()
    
    // Load existing tasks
    const tasks = await loadTasks()
    
    // Initialize task status
    tasks.set(taskId, {
      task_id: taskId,
      status: "pending",
      message: "Project generation queued"
    })
    
    // Save tasks
    await saveTasks(tasks)
    
    // Start background generation
    generateProjectBackground(taskId, config)
    
    return NextResponse.json({
      task_id: taskId,
      status: "pending",
      message: "Project generation started"
    })
    
  } catch (error) {
    console.error('Generation error:', error)
    return NextResponse.json(
      { detail: "Failed to generate project" },
      { status: 500 }
    )
  }
}

async function generateProjectBackground(taskId, config) {
  try {
    // Load tasks and update status
    const tasks = await loadTasks()
    const task = tasks.get(taskId)
    task.status = "processing"
    task.message = "Generating project structure..."
    await saveTasks(tasks)
    
    // Create temporary directory
    const projectDir = path.join(TEMP_DIR, taskId)
    await fs.mkdir(projectDir, { recursive: true })
    
    // Generate project using existing renderer
    const generatorPath = path.join(process.cwd(), '..', 'generator')
    const scriptPath = path.join(generatorPath, 'cli.py')
    
    // Execute the generator
    const command = `set PYTHONIOENCODING=utf-8 && set PYTHONLEGACYWINDOWSSTDIO=utf-8 && python "${scriptPath}" init --framework "${config.framework}" --task-type "${config.task_type}" --tracking "${config.experiment_tracking}" --orchestration "${config.orchestration}" --deployment "${config.deployment}" --monitoring "${config.monitoring}" --project-name "${config.project_name}" --author-name "${config.author_name}" --description "${config.description}"`
    
    const { stdout, stderr } = await execAsync(command, {
      cwd: projectDir,
      env: { ...process.env, PYTHONIOENCODING: 'utf-8', PYTHONLEGACYWINDOWSSTDIO: 'utf-8' }
    })
    
    if (stderr) {
      console.error('Generator stderr:', stderr)
    }
    
    // Create ZIP file
    const zipPath = path.join(TEMP_DIR, `${taskId}.zip`)
    await createZipFile(projectDir, zipPath)
    
    // Update status
    const updatedTasks = await loadTasks()
    const updatedTask = updatedTasks.get(taskId)
    updatedTask.status = "completed"
    updatedTask.message = "Project generated successfully"
    updatedTask.download_url = `/api/download/${taskId}`
    await saveTasks(updatedTasks)
    
  } catch (error) {
    console.error('Background generation error:', error)
    
    // Update status with error
    const tasks = await loadTasks()
    const task = tasks.get(taskId)
    task.status = "failed"
    task.message = `Generation failed: ${error.message}`
    await saveTasks(tasks)
    
    // Cleanup on failure
    try {
      const projectDir = path.join(TEMP_DIR, taskId)
      await fs.rm(projectDir, { recursive: true, force: true })
      
      const zipPath = path.join(TEMP_DIR, `${taskId}.zip`)
      await fs.rm(zipPath, { force: true })
    } catch (cleanupError) {
      console.error('Cleanup error:', cleanupError)
    }
  }
}

async function createZipFile(sourceDir, zipPath) {
  const archiver = require('archiver')
  const archive = archiver('zip', { zlib: { level: 9 } })
  
  return new Promise((resolve, reject) => {
    const output = require('fs').createWriteStream(zipPath)
    
    output.on('close', () => resolve())
    archive.on('error', (err) => reject(err))
    
    archive.pipe(output)
    archive.directory(sourceDir, false)
    archive.finalize()
  })
}
