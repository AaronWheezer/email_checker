"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Card } from "@/components/ui/card"
import { ShieldCheck, ShieldAlert, Loader2, Sparkles, RotateCcw } from "lucide-react"
import { cn } from "@/lib/utils"

type Result = 0 | 1 | null

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

    try {
      const base = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000"
      const url = base.endsWith("/predict") ? base : `${base.replace(/\/$/, "")}/predict`
      const res = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: emailContent })
      })
      const data = await res.json()
      // Map prediction: support numeric (1/0) and string ("spam"/"ham") responses
      let predicted: Result = null
      if (typeof data?.prediction === "number") {
        predicted = data.prediction === 1 ? 1 : 0
      } else if (typeof data?.prediction === "string") {
        const p = (data.prediction as string).toLowerCase().trim()
        // Support string labels: "spam"/"ham" and numeric strings: "1"/"0"
        if (p === "spam" || p === "1") predicted = 1
        else if (p === "ham" || p === "0") predicted = 0
        else predicted = null
      }
      const conf = typeof data?.confidence === "number" ? data.confidence : null
      setResult(predicted)
      setConfidence(conf)
    } catch (e) {
      setResult(null)
      setConfidence(null)
    }
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
            {(result !== null || !!emailContent) && (
              <Button onClick={handleReset} variant="outline" className="border-border bg-transparent">
                <RotateCcw className="w-4 h-4" />
              </Button>
            )}
          </div>
        </div>
      </Card>

      {result !== null && (
        <Card
          className={cn(
            "p-6 border-2 transition-all duration-300 animate-in fade-in slide-in-from-bottom-4",
            result === 1 ? "bg-destructive/15 border-destructive" : "bg-success/15 border-success"
          )}
        >
          <div className="flex items-center gap-4">
            <div
              className={cn(
                "w-14 h-14 rounded-full flex items-center justify-center",
                result === 1 ? "bg-destructive" : "bg-success",
              )}
            >
              {result === 0 ? (
                <ShieldCheck className="w-7 h-7 text-success-foreground" />
              ) : (
                <ShieldAlert className="w-7 h-7 text-destructive-foreground" />
              )}
            </div>
            <div className="flex-1">
              <h3 className="text-xl font-semibold text-foreground">
                {result === 0 ? "Legitimate Email" : "Spam Detected"}
              </h3>
              <p className="text-sm text-muted-foreground mt-1">
                {result === 0
                  ? "This email appears to be legitimate and safe."
                  : "This email shows characteristics of spam or phishing."}
              </p>
            </div>
            {typeof confidence === "number" && (
              <div className="text-right">
                <p className="text-sm font-medium text-foreground">{confidence.toFixed(1)}%</p>
                <p className="text-[10px] text-muted-foreground">Confidence</p>
              </div>
            )}
          </div>
        </Card>
      )}
    </div>
  )
}
