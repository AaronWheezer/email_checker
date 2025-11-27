import { EmailChecker } from "@/components/email-checker"
import { Header } from "@/components/header"
import { Features } from "@/components/features"

export default function Home() {
  return (
    <main className="min-h-screen bg-background">
      <Header />
      <div className="container mx-auto px-4 py-12 md:py-20">
        <div className="mx-auto max-w-3xl text-center mb-12">
          <p className="text-sm font-medium text-muted-foreground mb-4 tracking-wide uppercase">AI-Powered Detection</p>
          <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold tracking-tight text-foreground mb-6 text-balance">
            Spam or Ham?
          </h1>
          <p className="text-lg text-muted-foreground max-w-xl mx-auto leading-relaxed">
            Paste your email content below and let our machine learning model determine if it's legitimate or spam.
          </p>
        </div>
        <EmailChecker />
        <Features />
      </div>
    </main>
  )
}
