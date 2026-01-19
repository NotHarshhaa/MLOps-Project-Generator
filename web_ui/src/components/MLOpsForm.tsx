"use client"

import { useState, useEffect } from "react"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import * as z from "zod"
import axios from "axios"

// Use internal API routes
const API_URL = ""
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Form, FormControl, FormDescription, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { OptionCards } from "@/components/OptionCards"
import { Progress } from "@/components/ui/progress"
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { toast } from "sonner"
import { Loader2, Download, Rocket, Settings, Info, User, FileText, CheckCircle } from "lucide-react"

const formSchema = z.object({
  framework: z.string().optional(),
  task_type: z.string().optional(),
  experiment_tracking: z.string().optional(),
  orchestration: z.string().optional(),
  deployment: z.string().optional(),
  monitoring: z.string().optional(),
  project_name: z.string().min(1, "Project name is required").max(50, "Project name must be 50 characters or less"),
  author_name: z.string().min(1, "Author name is required").max(100, "Author name must be 100 characters or less"),
  description: z.string().min(1, "Description is required")
}).refine((data) => {
  // Custom validation: all option fields must be selected before submission
  const requiredFields = ['framework', 'task_type', 'experiment_tracking', 'orchestration', 'deployment', 'monitoring'] as const
  const missingFields = requiredFields.filter(field => !data[field])
  return missingFields.length === 0
}, {
  message: "Please select an option for all categories before generating your project",
  path: ["framework"] // Show error on first field
})

type FormValues = z.infer<typeof formSchema>

interface Option {
  value: string
  label: string
  description: string
}

interface Options {
  framework: Option[]
  task_type: Option[]
  experiment_tracking: Option[]
  orchestration: Option[]
  deployment: Option[]
  monitoring: Option[]
}

export default function MLOpsForm() {
  const [options, setOptions] = useState<Options | null>(null)
  const [isGenerating, setIsGenerating] = useState(false)
  const [taskId, setTaskId] = useState<string | null>(null)
  const [progress, setProgress] = useState(0)
  const [downloadUrl, setDownloadUrl] = useState<string | null>(null)
  const [showSuccessDialog, setShowSuccessDialog] = useState(false)

  const form = useForm<FormValues>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      framework: "",
      task_type: "",
      experiment_tracking: "",
      orchestration: "",
      deployment: "",
      monitoring: "",
      project_name: "",
      author_name: "MLOps Project Generator",
      description: "Generated using MLOps Project Generator - A comprehensive tool for creating production-ready machine learning projects with best practices and modern MLOps workflows."
    }
  })

  // Fetch options on component mount
  useEffect(() => {
    const fetchOptions = async () => {
      try {
        const response = await axios.get(`${API_URL}/api/options`)
        setOptions(response.data)
      } catch (error) {
        toast.error("Failed to load options. Please ensure the backend is running.")
      }
    }
    fetchOptions()
  }, [])

  const checkTaskStatus = async (taskId: string) => {
    try {
      const response = await axios.get(`${API_URL}/api/status/${taskId}`)
      const task = response.data
      
      if (task.status === "processing") {
        setProgress(50)
        setTimeout(() => checkTaskStatus(taskId), 2000)
      } else if (task.status === "completed") {
        setProgress(100)
        setDownloadUrl(task.download_url)
        setShowSuccessDialog(true)
        toast.success("Project generated successfully!")
        setIsGenerating(false)
      } else if (task.status === "failed") {
        toast.error(`Generation failed: ${task.message}`)
        setIsGenerating(false)
        setProgress(0)
      }
    } catch (error) {
      toast.error("Failed to check task status")
      setIsGenerating(false)
      setProgress(0)
    }
  }

  const onSubmit = async (values: FormValues) => {
    setIsGenerating(true)
    setProgress(10)
    
    try {
      const response = await axios.post(`${API_URL}/api/generate`, values)
      const task = response.data
      
      setTaskId(task.task_id)
      setProgress(25)
      toast.success("Project generation started!")
      
      // Start polling for status
      setTimeout(() => checkTaskStatus(task.task_id), 1000)
      
    } catch (error: any) {
      toast.error(error.response?.data?.detail || "Failed to generate project")
      setIsGenerating(false)
      setProgress(0)
    }
  }

  const handleDownload = () => {
    if (downloadUrl && taskId) {
      window.open(downloadUrl, "_blank")
      setShowSuccessDialog(false)
    }
  }

  const resetForm = () => {
    setShowSuccessDialog(false)
    setDownloadUrl(null)
    setTaskId(null)
    setProgress(0)
    form.reset()
    // Refresh options
    const fetchOptions = async () => {
      try {
        const response = await axios.get("/api/options")
        setOptions(response.data)
      } catch (error) {
        toast.error("Failed to refresh options.")
      }
    }
    fetchOptions()
  }

  if (!options) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <Loader2 className="h-8 w-8 animate-spin" />
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 p-3 sm:p-4 md:p-6 lg:p-8 overflow-x-hidden">
      <div className="w-full max-w-6xl mx-auto">
        {/* Header */}
        <div className="text-center mb-4 sm:mb-6 lg:mb-8 pt-4 sm:pt-6 lg:pt-8">
          <div className="flex items-center justify-center mb-2 sm:mb-3 lg:mb-4">
            <Rocket className="h-8 w-8 sm:h-10 sm:w-10 lg:h-12 lg:w-12 text-blue-600 mr-1 sm:mr-2 lg:mr-3 flex-shrink-0" />
            <h1 className="text-xl sm:text-2xl lg:text-3xl xl:text-4xl font-bold text-gray-900 break-words">MLOps Project Generator</h1>
          </div>
          <p className="text-sm sm:text-base lg:text-lg text-gray-600 max-w-2xl mx-auto px-2 sm:px-4">
            Generate production-ready MLOps project templates with best practices built-in
          </p>
        </div>

        {/* Main Form */}
        <Card className="shadow-lg w-full overflow-hidden">
          <CardHeader className="pb-3 sm:pb-4 lg:pb-6 px-3 sm:px-4 lg:px-6">
            <CardTitle className="flex items-center text-base sm:text-lg lg:text-xl">
              <Settings className="h-4 w-4 sm:h-5 sm:w-5 mr-2 flex-shrink-0" />
              <span className="break-words">Project Configuration</span>
            </CardTitle>
            <CardDescription className="text-xs sm:text-sm lg:text-base">
              Choose your ML stack and deployment preferences
            </CardDescription>
          </CardHeader>
          <CardContent className="p-3 sm:p-4 lg:p-6">
            <Form {...form}>
              <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
                <div className="space-y-4 sm:space-y-6 lg:space-y-8">
                  {/* Framework Selection */}
                  <FormField
                    control={form.control}
                    name="framework"
                    render={({ field }) => (
                      <FormItem>
                        <OptionCards
                          options={options.framework}
                          value={field.value}
                          onChange={field.onChange}
                          title="ML Framework"
                          description="Choose the machine learning framework for your project"
                        />
                        <FormMessage />
                      </FormItem>
                    )}
                  />

                  {/* Two Column Layout for Desktop */}
                  <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 sm:gap-6 lg:gap-8">
                    {/* Task Type */}
                    <div className="w-full">
                      <FormField
                        control={form.control}
                        name="task_type"
                        render={({ field }) => (
                          <FormItem>
                            <OptionCards
                              options={options.task_type}
                              value={field.value}
                              onChange={field.onChange}
                              title="Task Type"
                              description="Select the type of machine learning task"
                            />
                            <FormMessage />
                          </FormItem>
                        )}
                      />
                    </div>

                    {/* Experiment Tracking */}
                    <div className="w-full">
                      <FormField
                        control={form.control}
                        name="experiment_tracking"
                        render={({ field }) => (
                          <FormItem>
                            <OptionCards
                              options={options.experiment_tracking}
                              value={field.value}
                              onChange={field.onChange}
                              title="Experiment Tracking"
                              description="Choose how to track your ML experiments"
                            />
                            <FormMessage />
                          </FormItem>
                        )}
                      />
                    </div>
                  </div>

                  {/* Two Column Layout for Desktop */}
                  <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 sm:gap-6 lg:gap-8">
                    {/* Orchestration */}
                    <div className="w-full">
                      <FormField
                        control={form.control}
                        name="orchestration"
                        render={({ field }) => (
                          <FormItem>
                            <OptionCards
                              options={options.orchestration}
                              value={field.value}
                              onChange={field.onChange}
                              title="Orchestration"
                              description="Select workflow orchestration for your ML pipelines"
                            />
                            <FormMessage />
                          </FormItem>
                        )}
                      />
                    </div>

                    {/* Deployment */}
                    <div className="w-full">
                      <FormField
                        control={form.control}
                        name="deployment"
                        render={({ field }) => (
                          <FormItem>
                            <OptionCards
                              options={options.deployment}
                              value={field.value}
                              onChange={field.onChange}
                              title="Deployment"
                              description="Choose how to deploy your ML model"
                            />
                            <FormMessage />
                          </FormItem>
                        )}
                      />
                    </div>
                  </div>

                  {/* Monitoring - Full Width */}
                  <FormField
                    control={form.control}
                    name="monitoring"
                    render={({ field }) => (
                      <FormItem>
                        <OptionCards
                          options={options.monitoring}
                          value={field.value}
                          onChange={field.onChange}
                          title="Monitoring"
                          description="Select monitoring solution for your ML models"
                        />
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                </div>

                {/* Enhanced Separator */}
                <div className="border-t border-gray-200 pt-4 sm:pt-6 lg:pt-8">
                  <div className="flex items-center space-x-2 sm:space-x-3">
                    <div className="w-6 h-6 sm:w-8 sm:h-8 rounded-full bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center flex-shrink-0">
                      <Settings className="w-3 h-3 sm:w-4 sm:h-4 text-white" />
                    </div>
                    <div className="min-w-0 flex-1">
                      <h3 className="text-base sm:text-lg font-semibold text-gray-900 break-words">Project Details</h3>
                      <p className="text-xs sm:text-sm text-gray-600">Configure your project metadata</p>
                    </div>
                  </div>
                </div>

                {/* Enhanced Project Details */}
                <div className="space-y-3 sm:space-y-4 lg:space-y-6">
                  <div className="grid grid-cols-1 sm:grid-cols-1 lg:grid-cols-2 gap-3 sm:gap-4 lg:gap-6">
                    <FormField
                      control={form.control}
                      name="project_name"
                      render={({ field }) => (
                        <FormItem className="space-y-1 sm:space-y-2">
                          <FormLabel className="flex items-center space-x-1 sm:space-x-2">
                            <div className="w-4 h-4 sm:w-5 sm:h-5 rounded-lg bg-blue-100 flex items-center justify-center">
                              <Info className="w-2 h-2 sm:w-3 sm:h-3 text-blue-600" />
                            </div>
                            <span className="text-sm sm:text-base">Project Name</span>
                            <div className="group relative">
                              <div className="w-4 h-4 rounded-full bg-gray-200 flex items-center justify-center cursor-help">
                                <span className="text-xs text-gray-600">?</span>
                              </div>
                              <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-3 py-2 bg-gray-900 text-white text-sm rounded-lg opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap z-10">
                                <div className="absolute bottom-0 left-1/2 transform -translate-x-1/2 translate-y-1/2 rotate-45 w-2 h-2 bg-gray-900"></div>
                                Use lowercase, hyphens, and underscores only. Max 50 characters.
                              </div>
                            </div>
                          </FormLabel>
                          <FormControl>
                            <Input 
                              placeholder="my-ml-project" 
                              className="font-mono text-xs sm:text-sm h-8 sm:h-10"
                              {...field} 
                            />
                          </FormControl>
                          <FormDescription className="text-xs text-gray-500 hidden xs:block sm:block">
                            Examples: sentiment-analysis, image_classifier, sales-forecast
                          </FormDescription>
                          <FormMessage />
                        </FormItem>
                      )}
                    />

                    <FormField
                      control={form.control}
                      name="author_name"
                      render={({ field }) => (
                        <FormItem className="space-y-1 sm:space-y-2">
                          <FormLabel className="flex items-center space-x-1 sm:space-x-2">
                            <div className="w-4 h-4 sm:w-5 sm:h-5 rounded-lg bg-green-100 flex items-center justify-center">
                              <User className="w-2 h-2 sm:w-3 sm:h-3 text-green-600" />
                            </div>
                            <span className="text-sm sm:text-base">Author Name</span>
                          </FormLabel>
                          <FormControl>
                            <Input 
                              placeholder="Your Name" 
                              className="font-medium border-gray-200 focus:border-green-500 focus:ring-green-500 text-xs sm:text-sm h-8 sm:h-10"
                              {...field} 
                            />
                          </FormControl>
                          <FormDescription className="text-xs text-gray-500">
                            Your name or team name
                          </FormDescription>
                          <FormMessage />
                        </FormItem>
                      )}
                    />
                  </div>

                  <FormField
                    control={form.control}
                    name="description"
                    render={({ field }) => (
                      <FormItem className="space-y-1 sm:space-y-2">
                        <FormLabel className="flex items-center space-x-1 sm:space-x-2">
                          <div className="w-4 h-4 sm:w-5 sm:h-5 rounded-lg bg-purple-100 flex items-center justify-center">
                            <FileText className="w-2 h-2 sm:w-3 sm:h-3 text-purple-600" />
                          </div>
                          <span className="text-sm sm:text-base">Project Description</span>
                        </FormLabel>
                        <FormControl>
                          <Textarea
                            placeholder="A production-ready ML project for sentiment analysis using transformer models..."
                            className="min-h-[80px] sm:min-h-[100px] lg:min-h-[120px] resize-none border-gray-200 focus:border-purple-500 focus:ring-purple-500 text-sm sm:text-base"
                            {...field}
                          />
                        </FormControl>
                        <FormDescription className="text-xs text-gray-500">
                          <span className="hidden sm:inline">Brief description of your ML project, its purpose, and key features</span>
                          <span className="sm:hidden">Brief project description</span>
                        </FormDescription>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                </div>

                {/* Progress */}
                {isGenerating && (
                  <div className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span>Generating project...</span>
                      <span>{progress}%</span>
                    </div>
                    <Progress value={progress} className="w-full" />
                  </div>
                )}

                {/* Download Button */}
                {downloadUrl && (
                  <Button 
                    type="button" 
                    onClick={handleDownload}
                    className="w-full"
                    variant="outline"
                  >
                    <Download className="h-4 w-4 mr-2" />
                    Download Project
                  </Button>
                )}

                {/* Generate Button */}
                <Button 
                  type="submit" 
                  className="w-full"
                  disabled={isGenerating}
                  size="sm"
                >
                  {isGenerating ? (
                    <>
                      <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                      Generating...
                    </>
                  ) : (
                    <>
                      <Rocket className="h-4 w-4 mr-2" />
                      Generate Project
                    </>
                  )}
                </Button>
              </form>
            </Form>
          </CardContent>
        </Card>
        
        {/* Success Dialog */}
        <Dialog open={showSuccessDialog} onOpenChange={setShowSuccessDialog}>
          <DialogContent className="sm:max-w-md mx-3 sm:mx-4 max-w-[95vw]">
            <DialogHeader className="pb-3 sm:pb-4">
              <DialogTitle className="flex items-center space-x-1 sm:space-x-2 text-base sm:text-lg lg:text-xl">
                <CheckCircle className="h-4 w-4 sm:h-5 sm:w-5 lg:h-6 lg:w-6 text-green-600 flex-shrink-0" />
                <span className="text-base sm:text-lg lg:text-xl break-words">Project Generated Successfully!</span>
              </DialogTitle>
              <DialogDescription className="text-xs sm:text-sm text-gray-600">
                Thank you for using the MLOps Project Generator!
              </DialogDescription>
            </DialogHeader>
            <div className="flex flex-col space-y-3 sm:space-y-4">
              <div className="text-center p-2 sm:p-3 lg:p-4 bg-green-50 rounded-lg">
                <CheckCircle className="h-8 w-8 sm:h-10 sm:w-10 lg:h-12 lg:w-12 text-green-600 mx-auto mb-1 sm:mb-2" />
                <p className="text-xs sm:text-sm text-gray-600 px-1 sm:px-2">
                  Your MLOps project has been generated with best practices.
                </p>
              </div>
              <div className="flex flex-col sm:flex-row space-y-2 sm:space-y-0 sm:space-x-2 lg:space-x-3">
                <Button 
                  onClick={handleDownload}
                  className="w-full sm:flex-1 text-xs sm:text-sm"
                  size="sm"
                >
                  <Download className="h-3 w-3 sm:h-4 sm:w-4 mr-1 sm:mr-2" />
                  Download Project
                </Button>
                <Button 
                  onClick={resetForm}
                  variant="outline"
                  className="w-full sm:flex-1 text-xs sm:text-sm"
                  size="sm"
                >
                  Generate Another
                </Button>
              </div>
            </div>
          </DialogContent>
        </Dialog>
      </div>
    </div>
  )
}
