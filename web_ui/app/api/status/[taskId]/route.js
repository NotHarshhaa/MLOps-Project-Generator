import { NextResponse } from 'next/server'
import path from 'path'
import fs from 'fs/promises'

const TEMP_DIR = path.join(process.cwd(), 'temp', 'projects')
const TASKS_FILE = path.join(TEMP_DIR, 'tasks.json')

async function loadTasks() {
  try {
    const data = await fs.readFile(TASKS_FILE, 'utf8')
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
  
  return NextResponse.json(tasks.get(taskId))
}
