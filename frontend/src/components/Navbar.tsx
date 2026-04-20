"use client"

import Link from "next/link"
import NextImage from "next/image"
import { usePathname } from "next/navigation"
import { cn } from "@/lib/utils"
import { UserCircle2, Sparkles } from "lucide-react"

const modules = [
  { name: "Avatar", path: "/", icon: UserCircle2 },
]

export function Navbar() {
  const pathname = usePathname()

  return (
    <nav className="sticky top-0 z-50 w-full border-b border-slate-200 bg-white/80 backdrop-blur-md">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="flex h-16 items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-blue-600 text-white">
              <Sparkles className="h-5 w-5" />
            </div>
            <span className="text-xl font-bold tracking-tight text-slate-900">
              DreamTalk<span className="text-blue-600">Pro</span>
            </span>
          </div>
          
          <div className="hidden md:block">
            <div className="flex items-baseline space-x-4">
              {modules.map((module) => {
                const Icon = module.icon
                const isActive = pathname === module.path
                return (
                  <Link
                    key={module.name}
                    href={module.path}
                    className={cn(
                      "flex items-center gap-2 rounded-lg px-3 py-2 text-sm font-medium transition-colors",
                      isActive 
                        ? "bg-blue-50 text-blue-600" 
                        : "text-slate-600 hover:bg-slate-50 hover:text-slate-900"
                    )}
                  >
                    <Icon className="h-4 w-4" />
                    {module.name}
                  </Link>
                )
              })}
            </div>
          </div>
          
          <div className="flex items-center gap-4">
            <div className="relative h-8 w-8 rounded-full bg-slate-200 border border-slate-300 overflow-hidden shadow-inner">
              <NextImage src="https://api.dicebear.com/7.x/avataaars/svg?seed=Felix" alt="User" fill unoptimized />
            </div>
          </div>
        </div>
      </div>
    </nav>
  )
}
