import { Mail, Github } from "lucide-react"
import { Button } from "@/components/ui/button"

export function Header() {
  return (
    <header className="border-b border-border bg-background/80 backdrop-blur-sm sticky top-0 z-50">
      <div className="container mx-auto px-4 h-16 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-md bg-foreground flex items-center justify-center">
            <Mail className="w-4 h-4 text-background" />
          </div>
          <span className="font-semibold text-foreground">SpamCheck</span>
        </div>
        <nav className="hidden md:flex items-center gap-6">
          <a href="#features" className="text-sm text-muted-foreground hover:text-foreground transition-colors">
            Features
          </a>
          <a href="#api" className="text-sm text-muted-foreground hover:text-foreground transition-colors">
            API
          </a>
          <a href="#docs" className="text-sm text-muted-foreground hover:text-foreground transition-colors">
            Docs
          </a>
        </nav>
        <Button variant="outline" size="sm" className="gap-2 bg-transparent">
          <Github className="w-4 h-4" />
          <span className="hidden sm:inline">GitHub</span>
        </Button>
      </div>
    </header>
  )
}
