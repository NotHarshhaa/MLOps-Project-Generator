"use client"

import { Check, Brain, BarChart, Microscope, GitBranch, Rocket, Shield } from "lucide-react"
import { cn } from "@/lib/utils"

interface Option {
  value: string
  label: string
  description: string
}

interface OptionCardsProps {
  options: Option[]
  value: string | undefined
  onChange: (value: string) => void
  title: string
  description?: string
}

const getIcon = (title: string, value: string) => {
  switch (title) {
    case "ML Framework":
      switch (value) {
        case "sklearn": return Brain
        case "pytorch": return Rocket
        case "tensorflow": return Shield
        default: return Brain
      }
    case "Task Type":
      switch (value) {
        case "classification": return BarChart
        case "regression": return Brain
        case "timeseries": return Microscope
        default: return BarChart
      }
    case "Experiment Tracking":
      return Microscope
    case "Orchestration":
      return GitBranch
    case "Deployment":
      return Rocket
    case "Monitoring":
      return Shield
    default:
      return Brain
  }
}

export function OptionCards({ options, value, onChange, title, description }: OptionCardsProps) {
  const handleOptionClick = (optionValue: string) => {
    // Toggle: if already selected, deselect; otherwise select
    if (value === optionValue) {
      onChange("") // Deselect
    } else {
      onChange(optionValue) // Select
    }
  }

  return (
    <div className="space-y-4">
      <div>
        <h3 className="text-lg font-semibold text-gray-900">{title}</h3>
        {description && (
          <p className="text-sm text-gray-600 mt-1">{description}</p>
        )}
      </div>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2 sm:gap-3">
        {options.map((option) => {
          const Icon = getIcon(title, option.value)
          return (
            <OptionCard
              key={option.value}
              option={option}
              Icon={Icon}
              isSelected={value === option.value}
              onClick={() => handleOptionClick(option.value)}
            />
          )
        })}
      </div>
    </div>
  )
}

interface OptionCardProps {
  option: Option
  Icon: any
  isSelected: boolean
  onClick: () => void
}

function OptionCard({ option, Icon, isSelected, onClick }: OptionCardProps) {
  return (
    <div
      onClick={onClick}
      className={cn(
        "relative p-3 sm:p-4 rounded-lg border-2 cursor-pointer transition-all duration-200 hover:shadow-md group",
        isSelected
          ? "border-blue-500 bg-blue-50 shadow-sm hover:border-red-400 hover:bg-blue-50"
          : "border-gray-200 bg-white hover:border-gray-300"
      )}
    >
      {isSelected && (
        <div className="absolute top-2 right-2">
          <div className={cn(
            "w-5 h-5 sm:w-6 sm:h-6 rounded-full flex items-center justify-center transition-colors",
            "bg-blue-500 group-hover:bg-red-500"
          )}>
            <Check className="w-3 h-3 sm:w-4 sm:h-4 text-white" />
          </div>
        </div>
      )}
      
      <div className="space-y-2 sm:space-y-3">
        <div className="flex items-center space-x-2">
          <Icon className={cn(
            "w-4 h-4 sm:w-5 sm:h-5 transition-colors flex-shrink-0",
            isSelected 
              ? "text-blue-600 group-hover:text-red-600" 
              : "text-gray-400 group-hover:text-gray-600"
          )} />
          <h4 className={cn(
            "text-sm sm:text-base font-semibold transition-colors break-words",
            isSelected 
              ? "text-blue-900 group-hover:text-red-900" 
              : "text-gray-900"
          )}>
            {option.label}
          </h4>
        </div>
        <p className={cn(
          "text-xs sm:text-sm leading-relaxed transition-colors",
          isSelected 
            ? "text-blue-700 group-hover:text-red-700" 
            : "text-gray-600"
        )}>
          {option.description}
        </p>
        {isSelected && (
          <p className="text-xs text-red-600 font-medium mt-2 opacity-0 group-hover:opacity-100 transition-opacity">
            Click to deselect
          </p>
        )}
      </div>
    </div>
  )
}
