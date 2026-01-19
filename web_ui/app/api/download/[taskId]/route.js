import { NextResponse } from 'next/server'
import path from 'path'
import fs from 'fs'
import fsPromises from 'fs/promises'

const TEMP_DIR = path.join(process.cwd(), 'temp', 'projects')
const TASKS_FILE = path.join(TEMP_DIR, 'tasks.json')

async function loadTasks() {
  try {
    const data = await fsPromises.readFile(TASKS_FILE, 'utf8')
    return new Map(JSON.parse(data))
  } catch (error) {
    return new Map()
  }
}

export async function GET(request, { params }) {
  const { taskId } = await params
  
  const tasks = await loadTasks()
  
  if (!tasks.has(taskId)) {
    return NextResponse.json(
      { detail: "Task not found" },
      { status: 404 }
    )
  }
  
  const task = tasks.get(taskId)
  if (task.status !== "completed") {
    return NextResponse.json(
      { detail: "Project not ready for download" },
      { status: 400 }
    )
  }
  
  const zipPath = path.join(TEMP_DIR, `${taskId}.zip`)
  
  try {
    const fileBuffer = fs.readFileSync(zipPath)
    
    return new NextResponse(fileBuffer, {
      headers: {
        'Content-Type': 'application/zip',
        'Content-Disposition': `attachment; filename="${taskId}.zip"`,
        'Content-Length': fileBuffer.length.toString(),
      },
    })
  } catch (error) {
    return NextResponse.json(
      { detail: "Project file not found" },
      { status: 404 }
    )
  }
}
