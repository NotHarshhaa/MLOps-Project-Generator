"use client"

import { useState, useEffect } from "react"
import { useForm } from "react-hook-form"
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
import { ThemeToggle } from "@/components/theme-toggle"
import { toast } from "sonner"
import { Loader2, Download, Rocket, Settings, Info, User, FileText, CheckCircle, X, Brain, BarChart, Microscope, GitBranch, Shield, Cloud, Database, Palette, TrendingUp } from "lucide-react"

const formSchema = z.object({
  framework: z.string().optional(),
  task_type: z.string().optional(),
  experiment_tracking: z.string().optional(),
  orchestration: z.string().optional(),
  deployment: z.string().optional(),
  monitoring: z.string().optional(),
  cloud_provider: z.string().optional(),
  cloud_service: z.string().optional(),
  preset_config: z.string().optional(),
  custom_template: z.string().optional(),
  enable_analytics: z.boolean().optional(),
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
  cloud_provider: Option[]
  cloud_service: Option[]
  preset_config: Option[]
  custom_template: Option[]
}

export default function MLOpsForm() {
  const [options, setOptions] = useState<Options | null>(null)
  const [isGenerating, setIsGenerating] = useState(false)
  const [taskId, setTaskId] = useState<string | null>(null)
  const [progress, setProgress] = useState(0)
  const [downloadUrl, setDownloadUrl] = useState<string | null>(null)
  const [showSuccessDialog, setShowSuccessDialog] = useState(false)
  const [copiedEmail, setCopiedEmail] = useState(false)
  const [validationError, setValidationError] = useState<string | null>(null)

  
  const form = useForm<FormValues>({
    // resolver: zodResolver(formSchema), // Temporarily disabled for testing
    defaultValues: {
      framework: "",
      task_type: "",
      experiment_tracking: "",
      orchestration: "",
      deployment: "",
      monitoring: "",
      cloud_provider: "",
      cloud_service: "",
      preset_config: "",
      custom_template: "",
      enable_analytics: true,
      project_name: "",
      author_name: "MLOps Project Generator",
      description: "Generated using MLOps Project Generator - A comprehensive tool for creating production-ready machine learning projects with best practices and modern MLOps workflows."
    }
  })

  const formValues = form.watch()

  // Reset cloud service when cloud provider changes
  useEffect(() => {
    const subscription = form.watch((value, { name }) => {
      if (name === 'cloud_provider') {
        form.setValue('cloud_service', '')
      }
    })
    return () => subscription.unsubscribe()
  }, [form])

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
        // Gradual progress updates during processing
        setProgress(prev => {
          if (prev < 40) return 40
          if (prev < 60) return 60
          if (prev < 80) return 80
          return prev + 5
        })
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
    try {
      
      // Check for missing required options
      const missingOptions = []
    
    if (!values.framework) missingOptions.push({ field: 'framework', name: 'ML Framework', icon: '🤖' })
      if (!values.task_type) missingOptions.push({ field: 'task_type', name: 'Task Type', icon: '🎯' })
      if (!values.experiment_tracking) missingOptions.push({ field: 'experiment_tracking', name: 'Experiment Tracking', icon: '📊' })
      if (!values.orchestration) missingOptions.push({ field: 'orchestration', name: 'Orchestration', icon: '⚙️' })
      if (!values.deployment) missingOptions.push({ field: 'deployment', name: 'Deployment', icon: '🚀' })
      if (!values.monitoring) missingOptions.push({ field: 'monitoring', name: 'Monitoring', icon: '📈' })
      
      // Note: Cloud provider, cloud service, preset_config, and custom_template are optional
      // so we don't include them in the required fields validation
      
      // Check for missing project details
      const missingDetails = []
      if (!values.project_name?.trim()) missingDetails.push({ field: 'project_name', name: 'Project Name', icon: '📝' })
      if (!values.author_name?.trim()) missingDetails.push({ field: 'author_name', name: 'Author Name', icon: '👤' })
      if (!values.description?.trim()) missingDetails.push({ field: 'description', name: 'Project Description', icon: '📄' })
      
      const allMissing = [...missingOptions, ...missingDetails]
      
      if (allMissing.length > 0) {
        // Set validation error message with all missing fields
        const missingFieldNames = allMissing.map(field => field.name).join(', ')
        const errorMessage = `⚠️ Please select all required options before generating!\n\nMissing: ${missingFieldNames}`
        setValidationError(errorMessage)
        
        // Auto-clear validation error after 8 seconds
        setTimeout(() => {
          setValidationError(null)
        }, 8000)
        
        // Highlight all missing fields and scroll to the first one
        setTimeout(() => {
          const firstMissing = allMissing[0]
          
          // Highlight all missing fields with enhanced effects
          allMissing.forEach(missingField => {
            const element = document.querySelector(`[data-field="${missingField.field}"]`)
            if (element) {
              element.classList.add(
                'bg-gradient-to-r', 'from-red-50', 'to-orange-50', 
                'dark:from-red-900/30', 'dark:to-orange-900/30',
                'border-2', 'border-red-300', 'dark:border-red-600',
                'shadow-lg', 'shadow-red-200', 'dark:shadow-red-900/30',
                'transform', 'scale-[1.02]',
                'transition-all', 'duration-300'
              )
            }
          })
          
          // Scroll to the first missing field
          const firstElement = document.querySelector(`[data-field="${firstMissing.field}"]`)
          if (firstElement) {
            firstElement.scrollIntoView({ behavior: 'smooth', block: 'center' })
          }
          
          // Remove highlights after 5 seconds
          setTimeout(() => {
            allMissing.forEach(missingField => {
              const element = document.querySelector(`[data-field="${missingField.field}"]`)
              if (element) {
                element.classList.remove(
                  'bg-gradient-to-r', 'from-red-50', 'to-orange-50', 
                  'dark:from-red-900/30', 'dark:to-orange-900/30',
                  'border-2', 'border-red-300', 'dark:border-red-600',
                  'shadow-lg', 'shadow-red-200', 'dark:shadow-red-900/30',
                  'transform', 'scale-[1.02]',
                  'transition-all', 'duration-300'
                )
              }
            })
          }, 5000)
        }, 100)
        
        return
      }
      
      // Clear any existing validation errors
      setValidationError(null)
      
      setIsGenerating(true)
      setProgress(5)
      
      // Simulate initialization
      await new Promise(resolve => setTimeout(resolve, 500))
      setProgress(15)
      
      const response = await axios.post(`${API_URL}/api/generate`, values)
      const task = response.data
      
      setTaskId(task.task_id)
      setProgress(30)
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

  const resetForm = async () => {
    setShowSuccessDialog(false)
    setDownloadUrl(null)
    setTaskId(null)
    setProgress(0)
    
    // Reset form to default values
    form.reset()
    
    // Show success toast
    toast.success("Form reset - Ready for new project!")
    
    // Refresh options to get latest data
    try {
      const response = await axios.get("/api/options")
      setOptions(response.data)
    } catch (error) {
      toast.error("Failed to refresh options.")
    }
    
    // Auto-focus on first field after a short delay
    setTimeout(() => {
      const firstInput = document.querySelector('input[type="text"]') as HTMLInputElement
      if (firstInput) {
        firstInput.focus()
      }
    }, 100)
  }

  const unselectAll = () => {
    form.setValue("framework", "")
    form.setValue("task_type", "")
    form.setValue("experiment_tracking", "")
    form.setValue("orchestration", "")
    form.setValue("deployment", "")
    form.setValue("monitoring", "")
    form.setValue("cloud_provider", "")
    form.setValue("cloud_service", "")
    form.setValue("preset_config", "")
    form.setValue("custom_template", "")
    form.setValue("enable_analytics", true)
    toast.success("All selections cleared")
  }

  if (!options) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <Loader2 className="h-8 w-8 animate-spin" />
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 dark:from-gray-950 dark:to-black p-3 sm:p-4 md:p-6 lg:p-8 overflow-x-hidden">
      <div className="w-full max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-4 sm:mb-6 lg:mb-8 pt-4 sm:pt-6 lg:pt-8 relative">
          <div className="absolute top-0 right-0 sm:top-4 sm:right-4">
            <ThemeToggle />
          </div>
          <div className="flex items-center justify-center mb-2 sm:mb-3 lg:mb-4 pr-12 sm:pr-0">
            <Rocket className="h-8 w-8 sm:h-10 sm:w-10 lg:h-12 lg:w-12 text-zinc-900 dark:text-zinc-100 mr-1 sm:mr-2 lg:mr-3 flex-shrink-0" />
            <h1 className="text-xl sm:text-2xl lg:text-3xl xl:text-4xl font-bold text-gray-900 dark:text-gray-100 break-words">MLOps Project Generator</h1>
          </div>
          <p className="text-sm sm:text-base lg:text-lg text-gray-600 dark:text-zinc-400 max-w-2xl mx-auto px-2 sm:px-4">
            A comprehensive CLI tool that generates production-ready MLOps project templates with cloud deployment, configuration management, and analytics.
          </p>
          
          {/* New Features Badges */}
          <div className="flex flex-wrap justify-center gap-2 mt-4 px-2 sm:px-4">
            <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200">
              <Cloud className="w-3 h-3 mr-1" />
              Cloud Deployment
            </span>
            <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200">
              <Database className="w-3 h-3 mr-1" />
              Config Presets
            </span>
            <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200">
              <TrendingUp className="w-3 h-3 mr-1" />
              Analytics
            </span>
            <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-200">
              <Palette className="w-3 h-3 mr-1" />
              Custom Templates
            </span>
          </div>
        </div>

        {/* Main Form */}
        <Card className="shadow-lg w-full overflow-hidden dark:bg-zinc-800/80">
          <CardHeader className="pb-3 sm:pb-4 lg:pb-6 px-3 sm:px-4 lg:px-6">
            <div className="flex items-center justify-between">
              <div className="flex-1">
                <div className="flex items-center space-x-3 pb-2">
                  <div className="w-8 h-8 rounded-lg bg-zinc-900 dark:bg-zinc-100 flex items-center justify-center flex-shrink-0">
                    <Settings className="w-4 h-4 text-white dark:text-zinc-900" />
                  </div>
                  <div className="min-w-0 flex-1">
                    <h3 className="text-xl font-bold text-gray-900 dark:text-zinc-100 break-words">Project Configuration</h3>
                    <p className="text-sm text-gray-600 dark:text-zinc-400 mt-0.5">Choose your ML stack and deployment preferences</p>
                  </div>
                </div>
              </div>
              <Button
                type="button"
                size="sm"
                onClick={unselectAll}
                className="ml-2 flex-shrink-0"
              >
                <X className="h-4 w-4 mr-1" />
                <span className="hidden sm:inline">Unselect All</span>
                <span className="sm:hidden">Clear</span>
              </Button>
            </div>
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
                      <FormItem data-field="framework">
                        <OptionCards
                          options={options.framework}
                          value={field.value}
                          onChange={field.onChange}
                          title="ML Framework"
                          description="Choose the machine learning framework for your project"
                        />
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
                          <FormItem data-field="task_type">
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
                          <FormItem data-field="experiment_tracking">
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
                          <FormItem data-field="orchestration">
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
                          <FormItem data-field="deployment">
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
                      <FormItem data-field="monitoring">
                        <OptionCards
                          options={options.monitoring}
                          value={field.value}
                          onChange={field.onChange}
                          title="Monitoring"
                          description="Select monitoring solution for your ML models"
                        />
                      </FormItem>
                    )}
                  />

                  {/* Cloud Deployment Section */}
                  <div className="border-t border-gray-200 dark:border-zinc-800 pt-4 sm:pt-6 lg:pt-8">
                    <div className="flex items-center space-x-3 pb-4">
                      <div className="w-8 h-8 rounded-lg bg-zinc-900 dark:bg-zinc-100 flex items-center justify-center flex-shrink-0">
                        <Cloud className="w-4 h-4 text-white dark:text-zinc-900" />
                      </div>
                      <div className="min-w-0 flex-1">
                        <h3 className="text-xl font-bold text-gray-900 dark:text-zinc-100 break-words">Cloud Deployment</h3>
                        <p className="text-sm text-gray-600 dark:text-zinc-400 mt-0.5">Optional: Generate cloud-specific deployment templates</p>
                      </div>
                    </div>
                  </div>

                  <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 sm:gap-6 lg:gap-8">
                    {/* Cloud Provider */}
                    <div className="w-full">
                      <FormField
                        control={form.control}
                        name="cloud_provider"
                        render={({ field }) => (
                          <FormItem data-field="cloud_provider">
                            <OptionCards
                              options={[
                                { value: "", label: "Select Cloud Provider", description: "Choose your cloud provider (optional)" },
                                { value: "aws", label: "Amazon Web Services", description: "Deploy to AWS with SageMaker, ECS, Lambda" },
                                { value: "gcp", label: "Google Cloud Platform", description: "Deploy to GCP with Vertex AI, Cloud Run" },
                                { value: "azure", label: "Microsoft Azure", description: "Deploy to Azure with ML Studio, Functions" }
                              ]}
                              value={field.value}
                              onChange={field.onChange}
                              title="Cloud Provider"
                              description="Choose your cloud provider (optional)"
                            />
                            <FormMessage />
                          </FormItem>
                        )}
                      />
                    </div>

                    {/* Cloud Service */}
                    <div className="w-full">
                      <FormField
                        control={form.control}
                        name="cloud_service"
                        render={({ field }) => {
                          const selectedProvider = formValues.cloud_provider
                          let serviceOptions = [{ value: "", label: "Select Cloud Provider First", description: "Choose a cloud provider above" }]
                          
                          if (selectedProvider === "aws") {
                            serviceOptions = [
                              { value: "", label: "Select AWS Service", description: "Choose an AWS service" },
                              { value: "sagemaker", "label": "SageMaker", "description": "AWS managed ML service" },
                              { value: "ecs", "label": "ECS", "description": "Elastic Container Service" },
                              { value: "lambda", "label": "Lambda", "description": "Serverless functions" }
                            ]
                          } else if (selectedProvider === "gcp") {
                            serviceOptions = [
                              { value: "", label: "Select GCP Service", "description": "Choose a GCP service" },
                              { value: "vertex-ai", "label": "Vertex AI", "description": "GCP unified ML platform" },
                              { value: "cloud-run", "label": "Cloud Run", "description": "Serverless containers" },
                              { value: "ai-platform", "label": "AI Platform", "description": "GCP ML training and deployment" }
                            ]
                          } else if (selectedProvider === "azure") {
                            serviceOptions = [
                              { value: "", label: "Select Azure Service", "description": "Choose an Azure service" },
                              { value: "ml-studio", "label": "Azure ML Studio", "description": "Azure ML workspace" },
                              { value: "container-instances", "label": "Container Instances", "description": "Azure container service" },
                              { value: "functions", "label": "Functions", "description": "Azure serverless functions" }
                            ]
                          }
                          
                          return (
                            <FormItem data-field="cloud_service">
                              <OptionCards
                                options={serviceOptions}
                                value={field.value}
                                onChange={field.onChange}
                                title="Cloud Service"
                                description="Choose the specific cloud service"
                              />
                              <FormMessage />
                            </FormItem>
                          )
                        }}
                      />
                    </div>
                  </div>

                  {/* Configuration & Templates Section */}
                  <div className="border-t border-gray-200 dark:border-zinc-800 pt-4 sm:pt-6 lg:pt-8">
                    <div className="flex items-center space-x-3 pb-4">
                      <div className="w-8 h-8 rounded-lg bg-zinc-900 dark:bg-zinc-100 flex items-center justify-center flex-shrink-0">
                        <Database className="w-4 h-4 text-white dark:text-zinc-900" />
                      </div>
                      <div className="min-w-0 flex-1">
                        <h3 className="text-xl font-bold text-gray-900 dark:text-zinc-100 break-words">Configuration & Templates</h3>
                        <p className="text-sm text-gray-600 dark:text-zinc-400 mt-0.5">Advanced configuration and template options</p>
                      </div>
                    </div>
                  </div>

                  <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 sm:gap-6 lg:gap-8">
                    {/* Preset Configuration */}
                    <div className="w-full">
                      <FormField
                        control={form.control}
                        name="preset_config"
                        render={({ field }) => (
                          <FormItem data-field="preset_config">
                            <OptionCards
                              options={[
                                { value: "", label: "Select Configuration", description: "Use your current selections" },
                                { value: "quick-start", label: "Quick Start", description: "Basic setup for rapid prototyping" },
                                { value: "production-ready", label: "Production Ready", description: "Enterprise-grade configuration" },
                                { value: "research", label: "Research", description: "Optimized for ML research projects" },
                                { value: "enterprise", label: "Enterprise", description: "Full enterprise MLOps stack" }
                              ]}
                              value={field.value}
                              onChange={field.onChange}
                              title="Configuration Preset"
                              description="Use a predefined configuration preset (optional)"
                            />
                            <FormMessage />
                          </FormItem>
                        )}
                      />
                    </div>

                    {/* Custom Template */}
                    <div className="w-full">
                      <FormField
                        control={form.control}
                        name="custom_template"
                        render={({ field }) => (
                          <FormItem data-field="custom_template">
                            <OptionCards
                              options={[
                                { value: "", label: "Select Template", description: "Use the standard framework template" },
                                { value: "minimal", label: "Minimal", description: "Lightweight template with essentials only" },
                                { value: "comprehensive", label: "Comprehensive", description: "Full-featured template with all options" },
                                { value: "microservice", label: "Microservice", "description": "Microservice-oriented template" }
                              ]}
                              value={field.value}
                              onChange={field.onChange}
                              title="Custom Template"
                              description="Choose a custom template variant (optional)"
                            />
                            <FormMessage />
                          </FormItem>
                        )}
                      />
                    </div>
                  </div>

                  {/* Analytics Toggle */}
                  <div className="border-t border-gray-200 dark:border-zinc-800 pt-4 sm:pt-6 lg:pt-8">
                    <div className="flex items-center space-x-3 pb-4">
                      <div className="w-8 h-8 rounded-lg bg-zinc-900 dark:bg-zinc-100 flex items-center justify-center flex-shrink-0">
                        <TrendingUp className="w-4 h-4 text-white dark:text-zinc-900" />
                      </div>
                      <div className="min-w-0 flex-1">
                        <h3 className="text-xl font-bold text-gray-900 dark:text-zinc-100 break-words">Analytics & Insights</h3>
                        <p className="text-sm text-gray-600 dark:text-zinc-400 mt-0.5">Enable project analytics and usage tracking</p>
                      </div>
                    </div>
                  </div>

                  <FormField
                    control={form.control}
                    name="enable_analytics"
                    render={({ field }) => (
                      <FormItem className="flex flex-row items-center justify-between rounded-lg border p-4 dark:border-zinc-700">
                        <div className="space-y-0.5">
                          <FormLabel className="text-base font-semibold">Enable Analytics</FormLabel>
                          <FormDescription className="text-sm">
                            Track project generation metrics and get insights about your MLOps projects
                          </FormDescription>
                        </div>
                        <FormControl>
                          <input
                            type="checkbox"
                            checked={field.value}
                            onChange={field.onChange}
                            className="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                          />
                        </FormControl>
                      </FormItem>
                    )}
                  />
                </div>

                {/* Enhanced Separator */}
                <div className="border-t border-gray-200 dark:border-zinc-800 pt-4 sm:pt-6 lg:pt-8">
                  <div className="flex items-center space-x-3 pb-2">
                    <div className="w-8 h-8 rounded-lg bg-zinc-900 dark:bg-zinc-100 flex items-center justify-center flex-shrink-0">
                      <Settings className="w-4 h-4 text-white dark:text-zinc-900" />
                    </div>
                    <div className="min-w-0 flex-1">
                      <h3 className="text-xl font-bold text-gray-900 dark:text-zinc-100 break-words">Project Details</h3>
                      <p className="text-sm text-gray-600 dark:text-zinc-400 mt-0.5">Configure your project metadata</p>
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
                        <FormItem className="space-y-1 sm:space-y-2" data-field="project_name">
                          <FormLabel className="flex items-center space-x-2 sm:space-x-3">
                            <div className="w-6 h-6 sm:w-7 sm:h-7 rounded-lg bg-zinc-900 dark:bg-zinc-100 flex items-center justify-center flex-shrink-0">
                              <Info className="w-3 h-3 sm:w-4 sm:h-4 text-white dark:text-zinc-900" />
                            </div>
                            <span className="text-base sm:text-lg font-semibold text-gray-900 dark:text-zinc-100">Project Name</span>
                            <div className="group relative">
                              <div className="w-4 h-4 rounded-full bg-gray-200 dark:bg-zinc-700 flex items-center justify-center cursor-help">
                                <span className="text-xs text-gray-600 dark:text-zinc-400">?</span>
                              </div>
                              <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-3 py-2 bg-gray-900 dark:bg-gray-100 text-white dark:text-gray-900 text-sm rounded-lg opacity-0 group-hover:opacity-100 transition-opacity z-50 max-w-sm">
                                <div className="absolute bottom-0 left-1/2 transform -translate-x-1/2 translate-y-1/2 rotate-45 w-2 h-2 bg-gray-900 dark:bg-gray-100"></div>
                                Use lowercase, hyphens, and underscores only. Max 50 characters.
                              </div>
                            </div>
                          </FormLabel>
                          <FormControl>
                            <Input 
                              placeholder="my-ml-project" 
                              className="font-mono text-sm sm:text-base lg:text-base h-10 sm:h-11"
                              {...field} 
                            />
                          </FormControl>
                          <FormDescription className="text-sm text-gray-500 dark:text-zinc-400 hidden xs:block sm:block">
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
                        <FormItem className="space-y-1 sm:space-y-2" data-field="author_name">
                          <FormLabel className="flex items-center space-x-2 sm:space-x-3">
                            <div className="w-6 h-6 sm:w-7 sm:h-7 rounded-lg bg-zinc-900 dark:bg-zinc-100 flex items-center justify-center flex-shrink-0">
                              <User className="w-3 h-3 sm:w-4 sm:h-4 text-white dark:text-zinc-900" />
                            </div>
                            <span className="text-base sm:text-lg font-semibold text-gray-900 dark:text-zinc-100">Author Name</span>
                          </FormLabel>
                          <FormControl>
                            <Input 
                              placeholder="Your Name" 
                              className="font-medium text-sm sm:text-base lg:text-base h-10 sm:h-11"
                              {...field} 
                            />
                          </FormControl>
                          <FormDescription className="text-sm text-gray-500 dark:text-zinc-400">
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
                      <FormItem className="space-y-1 sm:space-y-2" data-field="description">
                        <FormLabel className="flex items-center space-x-2 sm:space-x-3">
                          <div className="w-6 h-6 sm:w-7 sm:h-7 rounded-lg bg-zinc-900 dark:bg-zinc-100 flex items-center justify-center flex-shrink-0">
                            <FileText className="w-3 h-3 sm:w-4 sm:h-4 text-white dark:text-zinc-900" />
                          </div>
                          <span className="text-base sm:text-lg font-semibold text-gray-900 dark:text-zinc-100">Project Description</span>
                        </FormLabel>
                        <FormControl>
                          <Textarea
                            placeholder="A production-ready ML project for sentiment analysis using transformer models..."
                            className="min-h-[100px] sm:min-h-[120px] lg:min-h-[140px] resize-none text-sm sm:text-base lg:text-base"
                            {...field}
                          />
                        </FormControl>
                        <FormDescription className="text-sm text-gray-500 dark:text-zinc-400">
                          <span className="hidden sm:inline">Brief description of your ML project, its purpose, and key features</span>
                          <span className="sm:hidden">Brief project description</span>
                        </FormDescription>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                </div>

                {/* Enhanced Progress */}
                {isGenerating && (
                  <div className="space-y-4">
                    <div className="bg-gray-50 dark:bg-zinc-900/50 rounded-xl p-4 sm:p-6 border border-gray-200 dark:border-zinc-700">
                      <div className="flex items-center justify-between mb-4">
                        <div className="flex items-center space-x-3">
                          <div className="relative">
                            <Loader2 className="h-5 w-5 sm:h-6 sm:w-6 text-zinc-900 dark:text-zinc-100 animate-spin" />
                            <div className="absolute inset-0 h-5 w-5 sm:h-6 sm:w-6 bg-zinc-900 dark:bg-zinc-100 rounded-full animate-ping opacity-20"></div>
                          </div>
                          <div>
                            <h3 className="text-base sm:text-lg font-semibold text-gray-900 dark:text-zinc-100">
                              {progress < 25 && "🚀 Initializing project generation..."}
                              {progress >= 25 && progress < 50 && "📁 Creating project structure..."}
                              {progress >= 50 && progress < 75 && "⚙️ Configuring MLOps components..."}
                              {progress >= 75 && progress < 100 && "🔧 Finalizing setup..."}
                              {progress === 100 && "✨ Project ready!"}
                            </h3>
                            <p className="text-sm text-gray-600 dark:text-zinc-400 mt-1">
                              Building your production-ready MLOps project
                            </p>
                          </div>
                        </div>
                        <div className="flex items-center space-x-2">
                          <span className="text-sm sm:text-base font-bold text-zinc-900 dark:text-zinc-100">
                            {progress}%
                          </span>
                          <div className="w-2 h-2 rounded-full bg-green-500 dark:bg-green-400 animate-pulse"></div>
                        </div>
                      </div>
                      
                      <div className="space-y-3">
                        <div className="relative">
                          <Progress value={progress} className="w-full h-3 sm:h-4" />
                          <div className="absolute top-0 left-0 h-full w-full bg-gradient-to-r from-transparent via-zinc-200 dark:via-zinc-700 to-transparent opacity-30 animate-pulse"></div>
                        </div>
                        
                        <div className="grid grid-cols-4 gap-2 sm:gap-3">
                          <div className={`text-center p-2 rounded-lg border transition-all ${
                            progress >= 0 ? 'bg-green-100 dark:bg-green-900/30 border-green-300 dark:border-green-700' : 'bg-gray-100 dark:bg-zinc-800 border-gray-300 dark:border-zinc-600'
                          }`}>
                            <div className={`w-2 h-2 rounded-full mx-auto mb-1 ${
                              progress >= 0 ? 'bg-green-500 dark:bg-green-400' : 'bg-gray-400 dark:bg-zinc-500'
                            }`}></div>
                            <p className="text-xs font-medium text-gray-700 dark:text-zinc-300">Init</p>
                          </div>
                          <div className={`text-center p-2 rounded-lg border transition-all ${
                            progress >= 25 ? 'bg-blue-100 dark:bg-blue-900/30 border-blue-300 dark:border-blue-700' : 'bg-gray-100 dark:bg-zinc-800 border-gray-300 dark:border-zinc-600'
                          }`}>
                            <div className={`w-2 h-2 rounded-full mx-auto mb-1 ${
                              progress >= 25 ? 'bg-blue-500 dark:bg-blue-400' : 'bg-gray-400 dark:bg-zinc-500'
                            }`}></div>
                            <p className="text-xs font-medium text-gray-700 dark:text-zinc-300">Build</p>
                          </div>
                          <div className={`text-center p-2 rounded-lg border transition-all ${
                            progress >= 50 ? 'bg-purple-100 dark:bg-purple-900/30 border-purple-300 dark:border-purple-700' : 'bg-gray-100 dark:bg-zinc-800 border-gray-300 dark:border-zinc-600'
                          }`}>
                            <div className={`w-2 h-2 rounded-full mx-auto mb-1 ${
                              progress >= 50 ? 'bg-purple-500 dark:bg-purple-400' : 'bg-gray-400 dark:bg-zinc-500'
                            }`}></div>
                            <p className="text-xs font-medium text-gray-700 dark:text-zinc-300">Config</p>
                          </div>
                          <div className={`text-center p-2 rounded-lg border transition-all ${
                            progress >= 75 ? 'bg-orange-100 dark:bg-orange-900/30 border-orange-300 dark:border-orange-700' : 'bg-gray-100 dark:bg-zinc-800 border-gray-300 dark:border-zinc-600'
                          }`}>
                            <div className={`w-2 h-2 rounded-full mx-auto mb-1 ${
                              progress >= 75 ? 'bg-orange-500 dark:bg-orange-400' : 'bg-gray-400 dark:bg-zinc-500'
                            }`}></div>
                            <p className="text-xs font-medium text-gray-700 dark:text-zinc-300">Final</p>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                )}

                
                {/* Project Summary - Only show when options are selected */}
                {(formValues.framework || formValues.task_type || formValues.experiment_tracking || formValues.orchestration || formValues.deployment || formValues.monitoring || formValues.cloud_provider || formValues.cloud_service || formValues.preset_config || formValues.custom_template || formValues.enable_analytics || formValues.project_name || formValues.author_name || formValues.description) && (
                  <div className="border-t border-gray-200 dark:border-zinc-800 pt-6 sm:pt-8">
                    <div className="flex items-center space-x-3 pb-3">
                      <div className="w-8 h-8 rounded-lg bg-zinc-900 dark:bg-zinc-100 flex items-center justify-center flex-shrink-0">
                        <FileText className="w-4 h-4 text-white dark:text-zinc-900" />
                      </div>
                      <div>
                        <h3 className="text-xl font-bold text-gray-900 dark:text-zinc-100">Project Summary</h3>
                        <p className="text-sm text-gray-600 dark:text-zinc-400 mt-0.5">Review your selections before generating</p>
                      </div>
                    </div>
                  
                  <div className="bg-white dark:bg-black border border-gray-200 dark:border-zinc-700 rounded-lg p-3 sm:p-4 sm:p-6 space-y-3 sm:space-y-4 sm:space-y-6">
                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 sm:gap-4 sm:gap-6">
                      <div className="bg-white dark:bg-black rounded-lg p-2 sm:p-3 border border-gray-200 dark:border-zinc-700">
                        <div className="flex items-center space-x-2 mb-2">
                          <div className="w-5 h-5 rounded-lg bg-zinc-900 dark:bg-zinc-100 flex items-center justify-center flex-shrink-0">
                            <Brain className="w-3 h-3 text-white dark:text-zinc-900" />
                          </div>
                          <h4 className="text-xs font-bold text-gray-800 dark:text-zinc-200 uppercase tracking-wide">ML Framework</h4>
                        </div>
                        <p className="text-base font-semibold text-gray-900 dark:text-zinc-100">
                          {formValues.framework || <span className="text-gray-400 dark:text-zinc-500 italic">Not selected</span>}
                        </p>
                      </div>
                      <div className="bg-white dark:bg-black rounded-lg p-2 sm:p-3 border border-gray-200 dark:border-zinc-700">
                        <div className="flex items-center space-x-2 mb-2">
                          <div className="w-5 h-5 rounded-lg bg-zinc-900 dark:bg-zinc-100 flex items-center justify-center flex-shrink-0">
                            <BarChart className="w-3 h-3 text-white dark:text-zinc-900" />
                          </div>
                          <h4 className="text-xs font-bold text-gray-800 dark:text-zinc-200 uppercase tracking-wide">Task Type</h4>
                        </div>
                        <p className="text-base font-semibold text-gray-900 dark:text-zinc-100">
                          {formValues.task_type || <span className="text-gray-400 dark:text-zinc-500 italic">Not selected</span>}
                        </p>
                      </div>
                      <div className="bg-white dark:bg-black rounded-lg p-2 sm:p-3 border border-gray-200 dark:border-zinc-700">
                        <div className="flex items-center space-x-2 mb-2">
                          <div className="w-5 h-5 rounded-lg bg-zinc-900 dark:bg-zinc-100 flex items-center justify-center flex-shrink-0">
                            <Microscope className="w-3 h-3 text-white dark:text-zinc-900" />
                          </div>
                          <h4 className="text-xs font-bold text-gray-800 dark:text-zinc-200 uppercase tracking-wide">Experiment Tracking</h4>
                        </div>
                        <p className="text-base font-semibold text-gray-900 dark:text-zinc-100">
                          {formValues.experiment_tracking || <span className="text-gray-400 dark:text-zinc-500 italic">Not selected</span>}
                        </p>
                      </div>
                      <div className="bg-white dark:bg-black rounded-lg p-2 sm:p-3 border border-gray-200 dark:border-zinc-700">
                        <div className="flex items-center space-x-2 mb-2">
                          <div className="w-5 h-5 rounded-lg bg-zinc-900 dark:bg-zinc-100 flex items-center justify-center flex-shrink-0">
                            <GitBranch className="w-3 h-3 text-white dark:text-zinc-900" />
                          </div>
                          <h4 className="text-xs font-bold text-gray-800 dark:text-zinc-200 uppercase tracking-wide">Orchestration</h4>
                        </div>
                        <p className="text-base font-semibold text-gray-900 dark:text-zinc-100">
                          {formValues.orchestration || <span className="text-gray-400 dark:text-zinc-500 italic">Not selected</span>}
                        </p>
                      </div>
                      <div className="bg-white dark:bg-black rounded-lg p-2 sm:p-3 border border-gray-200 dark:border-zinc-700">
                        <div className="flex items-center space-x-2 mb-2">
                          <div className="w-5 h-5 rounded-lg bg-zinc-900 dark:bg-zinc-100 flex items-center justify-center flex-shrink-0">
                            <Rocket className="w-3 h-3 text-white dark:text-zinc-900" />
                          </div>
                          <h4 className="text-xs font-bold text-gray-800 dark:text-zinc-200 uppercase tracking-wide">Deployment</h4>
                        </div>
                        <p className="text-base font-semibold text-gray-900 dark:text-zinc-100">
                          {formValues.deployment || <span className="text-gray-400 dark:text-zinc-500 italic">Not selected</span>}
                        </p>
                      </div>
                      <div className="bg-white dark:bg-black rounded-lg p-2 sm:p-3 border border-gray-200 dark:border-zinc-700">
                        <div className="flex items-center space-x-2 mb-2">
                          <div className="w-5 h-5 rounded-lg bg-zinc-900 dark:bg-zinc-100 flex items-center justify-center flex-shrink-0">
                            <Shield className="w-3 h-3 text-white dark:text-zinc-900" />
                          </div>
                          <h4 className="text-xs font-bold text-gray-800 dark:text-zinc-200 uppercase tracking-wide">Monitoring</h4>
                        </div>
                        <p className="text-base font-semibold text-gray-900 dark:text-zinc-100">
                          {formValues.monitoring || <span className="text-gray-400 dark:text-zinc-500 italic">Not selected</span>}
                        </p>
                      </div>
                    </div>
                    
                    {/* New v1.0.7 Features Summary */}
                    {(formValues.cloud_provider || formValues.cloud_service || formValues.preset_config || formValues.custom_template || formValues.enable_analytics) && (
                      <div className="border-t border-gray-300 dark:border-zinc-600 pt-4 sm:pt-6">
                        <div className="flex items-center space-x-2 mb-3 sm:mb-4">
                          <div className="w-5 h-5 rounded-lg bg-zinc-900 dark:bg-zinc-100 flex items-center justify-center flex-shrink-0">
                            <Cloud className="w-3 h-3 text-white dark:text-zinc-900" />
                          </div>
                          <h4 className="text-base font-bold text-gray-800 dark:text-zinc-200 uppercase tracking-wide">Advanced Features</h4>
                        </div>
                        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-2 gap-2 sm:gap-3">
                          {formValues.cloud_provider && (
                            <div className="bg-white dark:bg-black rounded-lg p-2 sm:p-3 border border-gray-200 dark:border-zinc-700">
                              <div className="flex items-center space-x-2 mb-2">
                                <div className="w-4 h-4 rounded-lg bg-zinc-900 dark:bg-zinc-100 flex items-center justify-center flex-shrink-0">
                                  <Cloud className="w-2 h-2 text-white dark:text-zinc-900" />
                                </div>
                                <h5 className="text-xs font-bold text-gray-700 dark:text-zinc-300 uppercase tracking-wide">Cloud Provider</h5>
                              </div>
                              <p className="text-sm font-semibold text-gray-900 dark:text-zinc-100 capitalize">
                                {formValues.cloud_provider}
                              </p>
                            </div>
                          )}
                          {formValues.cloud_service && (
                            <div className="bg-white dark:bg-black rounded-lg p-2 sm:p-3 border border-gray-200 dark:border-zinc-700">
                              <div className="flex items-center space-x-2 mb-2">
                                <div className="w-4 h-4 rounded-lg bg-zinc-900 dark:bg-zinc-100 flex items-center justify-center flex-shrink-0">
                                  <Cloud className="w-2 h-2 text-white dark:text-zinc-900" />
                                </div>
                                <h5 className="text-xs font-bold text-gray-700 dark:text-zinc-300 uppercase tracking-wide">Cloud Service</h5>
                              </div>
                              <p className="text-sm font-semibold text-gray-900 dark:text-zinc-100 capitalize">
                                {formValues.cloud_service}
                              </p>
                            </div>
                          )}
                          {formValues.preset_config && (
                            <div className="bg-white dark:bg-black rounded-lg p-2 sm:p-3 border border-gray-200 dark:border-zinc-700">
                              <div className="flex items-center space-x-2 mb-2">
                                <div className="w-4 h-4 rounded-lg bg-zinc-900 dark:bg-zinc-100 flex items-center justify-center flex-shrink-0">
                                  <Database className="w-2 h-2 text-white dark:text-zinc-900" />
                                </div>
                                <h5 className="text-xs font-bold text-gray-700 dark:text-zinc-300 uppercase tracking-wide">Configuration</h5>
                              </div>
                              <p className="text-sm font-semibold text-gray-900 dark:text-zinc-100 capitalize">
                                {formValues.preset_config}
                              </p>
                            </div>
                          )}
                          {formValues.custom_template && (
                            <div className="bg-white dark:bg-black rounded-lg p-2 sm:p-3 border border-gray-200 dark:border-zinc-700">
                              <div className="flex items-center space-x-2 mb-2">
                                <div className="w-4 h-4 rounded-lg bg-zinc-900 dark:bg-zinc-100 flex items-center justify-center flex-shrink-0">
                                  <Palette className="w-2 h-2 text-white dark:text-zinc-900" />
                                </div>
                                <h5 className="text-xs font-bold text-gray-700 dark:text-zinc-300 uppercase tracking-wide">Template</h5>
                              </div>
                              <p className="text-sm font-semibold text-gray-900 dark:text-zinc-100 capitalize">
                                {formValues.custom_template}
                              </p>
                            </div>
                          )}
                          {formValues.enable_analytics && (
                            <div className="bg-white dark:bg-black rounded-lg p-2 sm:p-3 border border-gray-200 dark:border-zinc-700">
                              <div className="flex items-center space-x-2 mb-2">
                                <div className="w-4 h-4 rounded-lg bg-zinc-900 dark:bg-zinc-100 flex items-center justify-center flex-shrink-0">
                                  <TrendingUp className="w-2 h-2 text-white dark:text-zinc-900" />
                                </div>
                                <h5 className="text-xs font-bold text-gray-700 dark:text-zinc-300 uppercase tracking-wide">Analytics</h5>
                              </div>
                              <p className="text-sm font-semibold text-gray-900 dark:text-zinc-100">
                                Enabled
                              </p>
                            </div>
                          )}
                        </div>
                      </div>
                    )}
                    
                    {(formValues.project_name || formValues.author_name || formValues.description) && (
                      <div className="border-t border-gray-300 dark:border-zinc-600 pt-4 sm:pt-6">
                        <div className="flex items-center space-x-2 mb-3 sm:mb-4">
                          <div className="w-5 h-5 rounded-lg bg-zinc-900 dark:bg-zinc-100 flex items-center justify-center flex-shrink-0">
                            <FileText className="w-3 h-3 text-white dark:text-zinc-900" />
                          </div>
                          <h4 className="text-base font-bold text-gray-800 dark:text-zinc-200 uppercase tracking-wide">Project Details</h4>
                        </div>
                        <div className="bg-white dark:bg-black rounded-lg p-3 sm:p-4 border border-gray-200 dark:border-zinc-700 space-y-2 sm:space-y-3">
                          {formValues.project_name && (
                            <div className="flex items-start space-x-3">
                              <div className="w-4 h-4 rounded-lg bg-zinc-900 dark:bg-zinc-100 flex items-center justify-center mt-1 flex-shrink-0">
                                <Info className="w-2 h-2 text-white dark:text-zinc-900" />
                              </div>
                              <div>
                                <span className="text-xs font-bold text-gray-600 dark:text-zinc-400 uppercase tracking-wide">Project Name:</span>
                                <p className="text-base font-semibold text-gray-900 dark:text-zinc-100 mt-1">{formValues.project_name}</p>
                              </div>
                            </div>
                          )}
                          {formValues.author_name && (
                            <div className="flex items-start space-x-3">
                              <div className="w-4 h-4 rounded-lg bg-zinc-900 dark:bg-zinc-100 flex items-center justify-center mt-1 flex-shrink-0">
                                <User className="w-2 h-2 text-white dark:text-zinc-900" />
                              </div>
                              <div>
                                <span className="text-xs font-bold text-gray-600 dark:text-zinc-400 uppercase tracking-wide">Author:</span>
                                <p className="text-base font-semibold text-gray-900 dark:text-zinc-100 mt-1">{formValues.author_name}</p>
                              </div>
                            </div>
                          )}
                          {formValues.description && (
                            <div className="flex items-start space-x-3">
                              <div className="w-4 h-4 rounded-lg bg-zinc-900 dark:bg-zinc-100 flex items-center justify-center mt-1 flex-shrink-0">
                                <FileText className="w-2 h-2 text-white dark:text-zinc-900" />
                              </div>
                              <div>
                                <span className="text-xs font-bold text-gray-600 dark:text-zinc-400 uppercase tracking-wide">Description:</span>
                                <p className="text-base font-semibold text-gray-900 dark:text-zinc-100 leading-relaxed mt-1">{formValues.description}</p>
                              </div>
                            </div>
                          )}
                        </div>
                      </div>
                    )}
                  </div>
                </div>
                  )}
                
                {/* Generate Button */}
                <div className="mt-6">
                <Button 
                  type="submit" 
                  className="w-full h-12 text-base font-semibold"
                  disabled={isGenerating}
                  size="lg"
                >
                  {isGenerating ? (
                    <>
                      <Loader2 className="h-5 w-5 mr-2 animate-spin" />
                      Generating...
                    </>
                  ) : (
                    <>
                      <Rocket className="h-5 w-5 mr-2" />
                      Generate Project
                    </>
                  )}
                </Button>
                </div>
                </form>
            </Form>
          </CardContent>
        </Card>
        
        {/* Validation Error Message - Enhanced UI with Close Button */}
        {validationError && (
          <div className="mt-4 p-4 bg-gradient-to-r from-red-50 to-orange-50 dark:from-red-900/30 dark:to-orange-900/30 border border-red-200 dark:border-red-700 rounded-xl shadow-lg shadow-red-100 dark:shadow-red-900/20">
            <div className="flex items-start justify-between">
              <div className="flex items-start space-x-3 flex-1">
                <div className="flex-shrink-0">
                  <div className="w-6 h-6 rounded-full bg-red-500 dark:bg-red-400 flex items-center justify-center animate-pulse">
                    <svg className="w-3 h-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.732-.833-2.502 0L4.316 16.5c-.77.833.192 2.5 1.732 2.5z" />
                    </svg>
                  </div>
                </div>
                <div className="flex-1">
                  <h4 className="text-sm font-bold text-red-800 dark:text-red-200 mb-1">Validation Required</h4>
                  <p className="text-sm text-red-700 dark:text-red-300 whitespace-pre-line leading-relaxed">
                    {validationError}
                  </p>
                </div>
              </div>
              <button
                onClick={() => setValidationError(null)}
                className="flex-shrink-0 ml-4 p-1 rounded-lg hover:bg-red-100 dark:hover:bg-red-800/50 transition-colors group"
                aria-label="Close validation message"
              >
                <svg className="w-5 h-5 text-red-500 dark:text-red-400 group-hover:text-red-700 dark:group-hover:text-red-300 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
          </div>
        )}
        
        {/* About Creator */}
        <Card className="shadow-lg w-full overflow-hidden dark:bg-zinc-800/80 mt-6">
          <CardContent className="p-2 sm:p-3 sm:p-4 sm:p-6 sm:p-8">
            <div className="flex flex-col items-center space-y-2 sm:space-y-3 sm:flex-row sm:items-start sm:space-y-0 sm:space-x-6 lg:flex-row lg:items-center lg:space-x-8">
              {/* Profile Section */}
              <div className="flex flex-col items-center space-y-2 sm:space-y-4 lg:space-y-4 sm:w-auto lg:w-auto">
                <div className="relative group">
                  <img 
                    src="https://github.com/NotHarshhaa.png" 
                    alt="HARSHHAA" 
                    className="w-20 h-20 sm:w-20 sm:h-20 lg:w-28 lg:h-28 rounded-full border-4 border-white dark:border-zinc-700 shadow-xl transition-transform group-hover:scale-105"
                  />
                  <div className="absolute -bottom-2 -right-2 w-5 h-5 sm:w-6 sm:h-6 bg-zinc-900 dark:bg-zinc-100 rounded-full flex items-center justify-center">
                    <CheckCircle className="w-3 h-3 sm:w-4 sm:h-4 text-white dark:text-zinc-900" />
                  </div>
                </div>
                <div className="text-center sm:text-left lg:text-center">
                  <div className="flex items-center justify-center sm:justify-start lg:justify-center space-x-2 mb-1">
                    <h3 className="text-lg sm:text-xl lg:text-3xl font-bold text-gray-900 dark:text-zinc-100">HARSHHAA</h3>
                    <div className="w-2 h-2 bg-zinc-900 dark:bg-zinc-100 rounded-full"></div>
                  </div>
                  <p className="text-xs sm:text-sm text-gray-600 dark:text-zinc-400 font-medium">@NotHarshhaa</p>
                  <div className="flex items-center justify-center sm:justify-start lg:justify-center space-x-2 mt-1 sm:mt-2">
                    <span className="inline-flex items-center px-2 py-1 bg-zinc-100 dark:bg-zinc-800 text-zinc-700 dark:text-zinc-300 text-xs font-semibold rounded-full">
                      Open to collaborate
                    </span>
                  </div>
                </div>
              </div>
              
              {/* About Content */}
              <div className="flex-1 text-center sm:text-left lg:text-left">
                <div className="flex items-center justify-center sm:justify-start lg:justify-center space-x-2 sm:space-x-3 mb-2 sm:mb-4">
                  <div className="w-8 h-8 rounded-lg bg-zinc-900 dark:bg-zinc-100 flex items-center justify-center flex-shrink-0">
                    <User className="w-4 h-4 text-white dark:text-zinc-900" />
                  </div>
                  <h4 className="text-lg font-bold text-gray-900 dark:text-zinc-100">About Me</h4>
                </div>
                
                <div className="bg-gray-50 dark:bg-zinc-900/50 rounded-xl p-2 sm:p-3 sm:p-4 sm:p-6 border border-gray-200 dark:border-zinc-700 mb-3 sm:mb-4 sm:mb-6">
                  <p className="text-sm sm:text-base text-gray-700 dark:text-zinc-300 leading-relaxed mb-2 sm:mb-4 text-center sm:text-left">
                    <span className="font-bold text-gray-900 dark:text-white">DevOps Engineer & Automation Specialist</span> with expertise in building robust cloud infrastructure, CI/CD pipelines, and MLOps solutions. Passionate about driving innovation and efficiency through cutting-edge technology.
                  </p>
                  
                  <div className="flex flex-wrap justify-center gap-1 sm:gap-2 mb-2 sm:mb-4 sm:justify-start">
                    <span className="inline-flex items-center px-3 py-1 bg-zinc-100 dark:bg-zinc-800 text-zinc-700 dark:text-zinc-300 text-sm font-semibold rounded-lg">
                      Cloud Architecture
                    </span>
                    <span className="inline-flex items-center px-3 py-1 bg-zinc-100 dark:bg-zinc-800 text-zinc-700 dark:text-zinc-300 text-sm font-semibold rounded-lg">
                      DevOps
                    </span>
                    <span className="inline-flex items-center px-3 py-1 bg-zinc-100 dark:bg-zinc-800 text-zinc-700 dark:text-zinc-300 text-sm font-semibold rounded-lg">
                      MLOps
                    </span>
                    <span className="inline-flex items-center px-3 py-1 bg-zinc-100 dark:bg-zinc-800 text-zinc-700 dark:text-zinc-300 text-sm font-semibold rounded-lg">
                      CI/CD
                    </span>
                  </div>
                  
                  <div className="grid grid-cols-3 sm:grid-cols-3 gap-2 sm:gap-4 text-center">
                    <div className="bg-white dark:bg-zinc-800 rounded-lg p-2 sm:p-3 border border-gray-200 dark:border-zinc-600">
                      <div className="text-lg sm:text-2xl font-bold text-gray-900 dark:text-white">5+</div>
                      <p className="text-xs text-gray-600 dark:text-zinc-400 mt-0.5 sm:mt-1">Years Experience</p>
                    </div>
                    <div className="bg-white dark:bg-zinc-800 rounded-lg p-2 sm:p-3 border border-gray-200 dark:border-zinc-600">
                      <div className="text-lg sm:text-2xl font-bold text-gray-900 dark:text-white">50+</div>
                      <p className="text-xs text-gray-600 dark:text-zinc-400 mt-0.5 sm:mt-1">Projects Delivered</p>
                    </div>
                    <div className="bg-white dark:bg-zinc-800 rounded-lg p-2 sm:p-3 border border-gray-200 dark:border-zinc-600">
                      <div className="text-lg sm:text-2xl font-bold text-gray-900 dark:text-white">Global</div>
                      <p className="text-xs text-gray-600 dark:text-zinc-400 mt-0.5 sm:mt-1">Reach & Impact</p>
                    </div>
                  </div>
                </div>
                
                <div className="flex flex-col sm:flex-row items-center justify-between space-y-4 sm:space-y-0">
                  <div className="flex items-center space-x-4">
                    <a 
                      href="https://github.com/NotHarshhaa" 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="inline-flex items-center space-x-2 px-4 py-2 bg-zinc-900 dark:bg-zinc-100 text-white dark:text-zinc-900 rounded-lg hover:bg-zinc-800 dark:hover:bg-zinc-200 transition-all hover:scale-105"
                    >
                      <GitBranch className="w-4 h-4" />
                      <span className="text-sm font-medium">GitHub</span>
                    </a>
                    <a 
                      href="https://linkedin.com/in/NotHarshhaa" 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="inline-flex items-center space-x-2 px-4 py-2 bg-zinc-900 dark:bg-zinc-100 text-white dark:text-zinc-900 rounded-lg hover:bg-zinc-800 dark:hover:bg-zinc-200 transition-all hover:scale-105"
                    >
                      <User className="w-4 h-4" />
                      <span className="text-sm font-medium">LinkedIn</span>
                    </a>
                  </div>
                  
                  <div className="flex items-center space-x-2 text-sm text-gray-500 dark:text-zinc-400">
                    <Info className="w-4 h-4" />
                    <span>harshhaa03@gmail.com</span>
                    <button
                      onClick={async () => {
                        try {
                          await navigator.clipboard.writeText('harshhaa03@gmail.com')
                          setCopiedEmail(true)
                          setTimeout(() => setCopiedEmail(false), 2000)
                        } catch (err) {
                          console.error('Failed to copy email:', err)
                        }
                      }}
                      className="inline-flex items-center px-2 py-1 bg-zinc-100 dark:bg-zinc-800 text-zinc-700 dark:text-zinc-300 text-xs font-medium rounded hover:bg-zinc-200 dark:hover:bg-zinc-700 transition-colors"
                    >
                      {copiedEmail ? 'Copied!' : 'Copy'}
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
        
        {/* Success Dialog */}
        <Dialog open={showSuccessDialog} onOpenChange={(open) => {
          if (!open) {
            // Reset all form fields when dialog is closed
            form.reset();
            setShowSuccessDialog(false);
          } else {
            setShowSuccessDialog(true);
          }
        }}>
          <DialogContent className="sm:max-w-lg md:max-w-xl lg:max-w-2xl mx-auto sm:mx-3 sm:mx-4 max-w-[95vw]">
            <DialogHeader className="pb-2 sm:pb-4 sm:pb-6">
              <div className="flex items-center space-x-2 sm:space-x-3 mb-1 sm:mb-2">
                <div className="w-8 h-8 sm:w-10 sm:h-10 sm:w-12 sm:h-12 rounded-lg bg-zinc-900 dark:bg-zinc-100 flex items-center justify-center flex-shrink-0">
                  <CheckCircle className="w-4 h-4 sm:w-5 sm:h-5 sm:w-6 sm:h-6 text-white dark:text-zinc-900" />
                </div>
                <div>
                  <DialogTitle className="text-base sm:text-lg lg:text-2xl font-bold text-gray-900 dark:text-zinc-100">
                    Project Generated Successfully!
                  </DialogTitle>
                  <DialogDescription className="text-xs sm:text-sm text-gray-600 dark:text-zinc-400 mt-0.5 sm:mt-1">
                    Your production-ready MLOps project is ready
                  </DialogDescription>
                </div>
              </div>
            </DialogHeader>
            <div className="flex flex-col space-y-3 sm:space-y-4 sm:space-y-6">
              <div className="bg-gray-50 dark:bg-zinc-900/50 rounded-xl p-3 sm:p-4 sm:p-6 border border-gray-200 dark:border-zinc-700">
                <div className="flex flex-col md:flex-row items-center md:items-start space-y-3 sm:space-y-4 md:space-y-0 md:space-x-6">
                  <div className="flex-shrink-0">
                    <div className="w-16 h-16 sm:w-20 sm:w-24 sm:h-24 rounded-full bg-zinc-100 dark:bg-zinc-800 flex items-center justify-center">
                      <Rocket className="w-8 h-8 sm:w-10 sm:w-12 text-zinc-900 dark:text-zinc-100" />
                    </div>
                  </div>
                  <div className="flex-1 text-center md:text-left">
                    <h3 className="text-lg sm:text-xl sm:text-2xl font-bold text-gray-900 dark:text-zinc-100 mb-1 sm:mb-2">
                      🎉 Congratulations!
                    </h3>
                    <p className="text-sm sm:text-base sm:text-lg text-gray-700 dark:text-zinc-300 leading-relaxed mb-2 sm:mb-4">
                      Your MLOps project has been generated with best practices, optimized for production deployment and scalability.
                    </p>
                    <div className="flex flex-wrap justify-center md:justify-start gap-1 sm:gap-2">
                      <span className="inline-flex items-center px-2 py-1 sm:px-3 py-1 bg-zinc-100 dark:bg-zinc-800 text-zinc-700 dark:text-zinc-300 text-xs sm:text-sm font-semibold rounded-lg">
                        Production Ready
                      </span>
                      <span className="inline-flex items-center px-2 py-1 sm:px-3 py-1 bg-zinc-100 dark:bg-zinc-800 text-zinc-700 dark:text-zinc-300 text-xs sm:text-sm font-semibold rounded-lg">
                        Best Practices
                      </span>
                      <span className="inline-flex items-center px-2 py-1 sm:px-3 py-1 bg-zinc-100 dark:bg-zinc-800 text-zinc-700 dark:text-zinc-300 text-xs sm:text-sm font-semibold rounded-lg">
                        Scalable
                      </span>
                      <span className="inline-flex items-center px-2 py-1 sm:px-3 py-1 bg-zinc-100 dark:bg-zinc-800 text-zinc-700 dark:text-zinc-300 text-xs sm:text-sm font-semibold rounded-lg">
                        Cloud Native
                      </span>
                      <span className="inline-flex items-center px-2 py-1 sm:px-3 py-1 bg-zinc-100 dark:bg-zinc-800 text-zinc-700 dark:text-zinc-300 text-xs sm:text-sm font-semibold rounded-lg">
                        CI/CD Ready
                      </span>
                    </div>
                  </div>
                </div>
              </div>
              <div className="flex flex-col sm:flex-row space-y-3 sm:space-y-0 sm:space-x-3">
                <Button 
                  onClick={handleDownload}
                  className="w-full sm:flex-1 text-sm sm:text-base h-11 sm:h-12"
                  size="lg"
                >
                  <Download className="h-4 w-4 sm:h-5 sm:w-5 mr-2" />
                  Download Project
                </Button>
                <Button 
                  onClick={resetForm}
                  variant="outline"
                  className="w-full sm:flex-1 text-sm sm:text-base h-11 sm:h-12"
                  size="lg"
                >
                  <Settings className="h-4 w-4 sm:h-5 sm:w-5 mr-2" />
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
