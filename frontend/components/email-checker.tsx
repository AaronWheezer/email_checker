"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Card } from "@/components/ui/card"
import { ShieldCheck, ShieldAlert, Loader2, Sparkles, RotateCcw } from "lucide-react"
import { cn } from "@/lib/utils"

type Result = "spam" | "ham" | null

export function EmailChecker() {
  const [emailContent, setEmailContent] = useState("")
  const [result, setResult] = useState<Result>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [confidence, setConfidence] = useState<number | null>(null)

  const handleCheck = async () => {
    if (!emailContent.trim()) return

    setIsLoading(true)
    setResult(null)
    setConfidence(null)

    // Simulating API call to FastAPI backend
    // Replace this with actual API call when ready
    await new Promise((resolve) => setTimeout(resolve, 1500))

    // Mock result - replace with actual API response
    const mockResult: Result =
      emailContent.toLowerCase().includes("free") ||
      emailContent.toLowerCase().includes("winner") ||
      emailContent.toLowerCase().includes("click here")
        ? "spam"
        : "ham"
    const mockConfidence = Math.random() * 20 + 80 // 80-100%

    setResult(mockResult)
    setConfidence(mockConfidence)
    setIsLoading(false)
  }

  const handleReset = () => {
    setEmailContent("")
    setResult(null)
    setConfidence(null)
  }

  return (
    <div className="mx-auto max-w-2xl space-y-6">
      <Card className="p-6 bg-card border-border">
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <label htmlFor="email-content" className="text-sm font-medium text-foreground">
              Email Content
            </label>
            <span className="text-xs text-muted-foreground">{emailContent.length} characters</span>
          </div>
          <Textarea
            id="email-content"
            placeholder="Paste your email content here..."
            value={emailContent}
            onChange={(e) => setEmailContent(e.target.value)}
            className="min-h-[200px] bg-input border-border text-foreground placeholder:text-muted-foreground resize-none font-mono text-sm"
          />
          <div className="flex gap-3">
            <Button
              onClick={handleCheck}
              disabled={!emailContent.trim() || isLoading}
              className="flex-1 bg-foreground text-background hover:bg-foreground/90"
            >
              {isLoading ? (
                <>
                  <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                  Analyzing...
                </>
              ) : (
                <>
                  <Sparkles className="w-4 h-4 mr-2" />
                  Check Email
                </>
              )}
            </Button>
            {(result || emailContent) && (
              <Button onClick={handleReset} variant="outline" className="border-border bg-transparent">
                <RotateCcw className="w-4 h-4" />
              </Button>
            )}
          </div>
        </div>
      </Card>

      {result && (
        <Card
          className={cn(
            "p-6 border-2 transition-all duration-300 animate-in fade-in slide-in-from-bottom-4",
            result === "ham" ? "bg-success/10 border-success" : "bg-destructive/10 border-destructive",
          )}
        >
          <div className="flex items-center gap-4">
            <div
              className={cn(
                "w-14 h-14 rounded-full flex items-center justify-center",
                result === "ham" ? "bg-success" : "bg-destructive",
              )}
            >
              {result === "ham" ? (
                <ShieldCheck className="w-7 h-7 text-success-foreground" />
              ) : (
                <ShieldAlert className="w-7 h-7 text-destructive-foreground" />
              )}
            </div>
            <div className="flex-1">
              <h3 className="text-xl font-semibold text-foreground">
                {result === "ham" ? "Legitimate Email" : "Spam Detected"}
              </h3>
              <p className="text-sm text-muted-foreground mt-1">
                {result === "ham"
                  ? "This email appears to be legitimate and safe."
                  : "This email shows characteristics of spam or phishing."}
              </p>
            </div>
            {confidence && (
              <div className="text-right">
                <p className="text-2xl font-bold text-foreground">{confidence.toFixed(1)}%</p>
                <p className="text-xs text-muted-foreground">Confidence</p>
              </div>
            )}
          </div>
        </Card>
      )}
    </div>
  )
}
