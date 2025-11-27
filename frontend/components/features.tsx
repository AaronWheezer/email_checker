import { Cloud, Zap, Lock, Code } from "lucide-react"

const features = [
  {
    icon: Zap,
    title: "Real-time Analysis",
    description: "Get instant results powered by machine learning models trained on millions of emails.",
  },
  {
    icon: Cloud,
    title: "Cloud Deployed",
    description: "Deployed on Azure ML with Docker and Kubernetes for high availability.",
  },
  {
    icon: Lock,
    title: "Privacy First",
    description: "Your email content is never stored. All analysis happens in memory.",
  },
  {
    icon: Code,
    title: "API Ready",
    description: "FastAPI backend ready for integration with your existing applications.",
  },
]

export function Features() {
  return (
    <section id="features" className="mt-20 pt-12 border-t border-border">
      <div className="text-center mb-12">
        <h2 className="text-2xl md:text-3xl font-bold text-foreground mb-4">Built for Production</h2>
        <p className="text-muted-foreground max-w-lg mx-auto">
          Enterprise-grade spam detection with modern infrastructure.
        </p>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {features.map((feature) => (
          <div
            key={feature.title}
            className="p-6 rounded-lg bg-card border border-border hover:border-muted-foreground/50 transition-colors"
          >
            <div className="w-10 h-10 rounded-md bg-secondary flex items-center justify-center mb-4">
              <feature.icon className="w-5 h-5 text-foreground" />
            </div>
            <h3 className="font-semibold text-foreground mb-2">{feature.title}</h3>
            <p className="text-sm text-muted-foreground leading-relaxed">{feature.description}</p>
          </div>
        ))}
      </div>
    </section>
  )
}
