import Link from "next/link";
import {
  ArrowRight,
  FileText,
  History,
  MessageSquare,
  Pill,
  ShieldCheck,
  Sparkles,
  Check,
  Star,
  LayoutDashboard,
  ScanLine,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { LandingNavbar } from "@/components/landing/navbar-landing";

const benefits = [
  {
    icon: History,
    title: "One timeline, every record",
    description:
      "Visits, labs, procedures, and prescriptions from every provider, organized chronologically the moment you upload them.",
  },
  {
    icon: Sparkles,
    title: "AI reads the paperwork for you",
    description:
      "HealthVault AI extracts conditions, medications, and results from PDFs and photos, so you don't have to decode medical jargon.",
  },
  {
    icon: MessageSquare,
    title: "Ask, don't search",
    description:
      "\u201CWhen was my last A1c?\u201D Get a straight answer, pulled from your actual history, in seconds.",
  },
  {
    icon: ShieldCheck,
    title: "Built for your privacy",
    description:
      "Your records are encrypted end-to-end. You control exactly what gets shared, and with whom.",
  },
];

const steps = [
  { title: "Upload your records", description: "Drag in PDFs, scans, or photos from any provider or portal." },
  { title: "AI organizes everything", description: "We structure conditions, meds, allergies, and labs automatically." },
  { title: "See the full picture", description: "Browse your timeline, ask your assistant, or share a summary with a doctor." },
];

const pricingTiers = [
  {
    name: "Personal",
    price: "Free",
    description: "Everything you need to get your records in order.",
    features: ["Unlimited uploads", "AI-structured timeline", "Basic AI assistant", "Share with 1 physician"],
    cta: "Get started",
    highlighted: false,
  },
  {
    name: "Plus",
    price: "$9",
    period: "/month",
    description: "For anyone managing an ongoing condition.",
    features: [
      "Everything in Personal",
      "Unlimited physician sharing",
      "Lab trend charts & alerts",
      "Priority AI assistant",
      "Family member profiles",
    ],
    cta: "Start free trial",
    highlighted: true,
  },
  {
    name: "Family",
    price: "$19",
    period: "/month",
    description: "One vault for the whole household.",
    features: ["Everything in Plus", "Up to 6 member profiles", "Shared emergency contacts", "Caregiver access controls"],
    cta: "Start free trial",
    highlighted: false,
  },
];

const testimonials = [
  {
    quote:
      "I finally have every specialist visit from the last five years in one place. My new doctor was stunned by how organized my history was.",
    name: "Maria Chen",
    role: "Type 1 Diabetes, patient since 2023",
  },
  {
    quote:
      "The AI assistant answered a question about my dad's medications faster than I could find the paperwork. It's genuinely changed how we manage his care.",
    name: "Jordan Wells",
    role: "Caregiver",
  },
  {
    quote:
      "Uploading records used to feel like a chore. Now I just drop in the PDF and HealthVault does the rest — labs, dates, everything.",
    name: "Priya Nataraj",
    role: "Member since 2024",
  },
];

export default function LandingPage() {
  return (
    <div className="flex min-h-screen flex-col">
      <LandingNavbar />

      {/* Hero */}
      <section className="relative overflow-hidden">
        <div className="absolute inset-0 -z-10 bg-[radial-gradient(ellipse_at_top,_hsl(217,91%,97%),_transparent_60%)]" />
        <div className="container grid gap-12 py-20 lg:grid-cols-2 lg:items-center lg:py-28">
          <div>
            <div className="inline-flex items-center gap-2 rounded-full border border-border bg-card px-3 py-1 text-xs font-medium text-muted-foreground">
              <Sparkles className="h-3.5 w-3.5 text-teal" />
              Now with AI-generated summaries
            </div>
            <h1 className="mt-6 text-4xl font-semibold tracking-tight sm:text-5xl lg:text-6xl">
              Your medical history,
              <br />
              <span className="text-gradient-brand">finally understood.</span>
            </h1>
            <p className="mt-6 max-w-xl text-lg text-muted-foreground">
              HealthVault AI turns scattered records, PDFs, and portal exports into one clear
              timeline — with an AI assistant that actually knows your history.
            </p>
            <div className="mt-8 flex flex-col gap-3 sm:flex-row">
              <Link href="/register">
                <Button size="lg" className="w-full sm:w-auto">
                  Get started free
                  <ArrowRight className="h-4 w-4" />
                </Button>
              </Link>
              <Link href="/upload">
                <Button size="lg" variant="outline" className="w-full sm:w-auto">
                  Upload a record
                </Button>
              </Link>
            </div>
            <p className="mt-4 text-xs text-muted-foreground">No credit card required · HIPAA-conscious by design</p>
          </div>

          <div className="relative">
            <div className="rounded-2xl border border-border bg-card p-3 shadow-xl">
              <div className="rounded-xl border border-border bg-gradient-to-br from-primary/5 to-teal/5 p-6">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <LayoutDashboard className="h-4 w-4 text-primary" />
                    <span className="text-sm font-semibold">Dashboard preview</span>
                  </div>
                  <span className="rounded-full bg-success/10 px-2 py-0.5 text-[10px] font-medium text-success">Live</span>
                </div>
                <div className="mt-5 grid grid-cols-2 gap-3">
                  <div className="rounded-lg bg-card p-4 shadow-sm">
                    <p className="text-xs text-muted-foreground">Health Score</p>
                    <p className="mt-1 text-2xl font-semibold text-teal">86</p>
                  </div>
                  <div className="rounded-lg bg-card p-4 shadow-sm">
                    <p className="text-xs text-muted-foreground">A1c trend</p>
                    <p className="mt-1 text-2xl font-semibold text-primary">6.4%</p>
                  </div>
                </div>
                <div className="mt-3 space-y-2">
                  {["Type 2 Diabetes — chronic", "Hypertension — chronic", "Hyperlipidemia — chronic"].map((c) => (
                    <div key={c} className="flex items-center gap-2 rounded-lg bg-card px-3 py-2 shadow-sm text-xs">
                      <span className="h-1.5 w-1.5 rounded-full bg-warning" />
                      {c}
                    </div>
                  ))}
                </div>
              </div>
            </div>
            <div className="absolute -bottom-6 -left-6 hidden rounded-xl border border-border bg-card p-4 shadow-lg sm:block">
              <div className="flex items-center gap-2">
                <MessageSquare className="h-4 w-4 text-teal" />
                <p className="text-xs font-medium">"What were my latest labs?"</p>
              </div>
              <p className="mt-1 text-[11px] text-muted-foreground">Answered instantly from your timeline</p>
            </div>
          </div>
        </div>
      </section>

      {/* Benefits */}
      <section id="features" className="border-t border-border bg-muted/30 py-20">
        <div className="container">
          <div className="max-w-2xl">
            <h2 className="text-3xl font-semibold tracking-tight sm:text-4xl">Everything scattered, now in one vault</h2>
            <p className="mt-4 text-muted-foreground">
              Stop digging through portals and folders. HealthVault AI brings structure to
              records that were never designed to work together.
            </p>
          </div>
          <div className="mt-12 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
            {benefits.map((b) => (
              <div key={b.title} className="rounded-xl border border-border bg-card p-6 shadow-sm">
                <span className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary/10">
                  <b.icon className="h-5 w-5 text-primary" />
                </span>
                <h3 className="mt-4 text-sm font-semibold">{b.title}</h3>
                <p className="mt-2 text-sm text-muted-foreground">{b.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* How it works / demo screenshots */}
      <section id="how-it-works" className="py-20">
        <div className="container">
          <div className="max-w-2xl">
            <h2 className="text-3xl font-semibold tracking-tight sm:text-4xl">From PDF to insight in three steps</h2>
          </div>
          <div className="mt-12 grid gap-8 lg:grid-cols-3">
            {steps.map((s, i) => (
              <div key={s.title}>
                <div className="flex items-center gap-3">
                  <span className="flex h-8 w-8 items-center justify-center rounded-full gradient-brand text-sm font-semibold text-white">
                    {i + 1}
                  </span>
                  <h3 className="text-sm font-semibold">{s.title}</h3>
                </div>
                <p className="mt-3 text-sm text-muted-foreground">{s.description}</p>
                <div className="mt-4 flex h-40 items-center justify-center rounded-xl border border-dashed border-border bg-muted/50">
                  {i === 0 && <FileText className="h-8 w-8 text-muted-foreground/50" />}
                  {i === 1 && <ScanLine className="h-8 w-8 text-muted-foreground/50" />}
                  {i === 2 && <Pill className="h-8 w-8 text-muted-foreground/50" />}
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Pricing */}
      <section id="pricing" className="border-t border-border bg-muted/30 py-20">
        <div className="container">
          <div className="max-w-2xl">
            <h2 className="text-3xl font-semibold tracking-tight sm:text-4xl">Simple pricing, no surprises</h2>
            <p className="mt-4 text-muted-foreground">Start free. Upgrade when you need more from your record.</p>
          </div>
          <div className="mt-12 grid gap-6 lg:grid-cols-3">
            {pricingTiers.map((tier) => (
              <div
                key={tier.name}
                className={`rounded-2xl border p-8 ${
                  tier.highlighted
                    ? "border-primary bg-card shadow-xl ring-1 ring-primary"
                    : "border-border bg-card shadow-sm"
                }`}
              >
                {tier.highlighted && (
                  <span className="mb-4 inline-block rounded-full bg-primary/10 px-3 py-1 text-xs font-medium text-primary">
                    Most popular
                  </span>
                )}
                <h3 className="text-lg font-semibold">{tier.name}</h3>
                <p className="mt-1 text-sm text-muted-foreground">{tier.description}</p>
                <div className="mt-6 flex items-baseline gap-1">
                  <span className="text-4xl font-semibold tracking-tight">{tier.price}</span>
                  {tier.period && <span className="text-sm text-muted-foreground">{tier.period}</span>}
                </div>
                <ul className="mt-6 space-y-3">
                  {tier.features.map((f) => (
                    <li key={f} className="flex items-start gap-2 text-sm">
                      <Check className="mt-0.5 h-4 w-4 shrink-0 text-teal" />
                      {f}
                    </li>
                  ))}
                </ul>
                <Link href="/register">
                  <Button className="mt-8 w-full" variant={tier.highlighted ? "default" : "outline"}>
                    {tier.cta}
                  </Button>
                </Link>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Testimonials */}
      <section id="testimonials" className="py-20">
        <div className="container">
          <div className="max-w-2xl">
            <h2 className="text-3xl font-semibold tracking-tight sm:text-4xl">Trusted with what matters most</h2>
          </div>
          <div className="mt-12 grid gap-6 lg:grid-cols-3">
            {testimonials.map((t) => (
              <div key={t.name} className="rounded-xl border border-border bg-card p-6 shadow-sm">
                <div className="flex gap-0.5 text-teal">
                  {Array.from({ length: 5 }).map((_, i) => (
                    <Star key={i} className="h-3.5 w-3.5 fill-current" />
                  ))}
                </div>
                <p className="mt-4 text-sm leading-relaxed text-foreground">"{t.quote}"</p>
                <div className="mt-5">
                  <p className="text-sm font-semibold">{t.name}</p>
                  <p className="text-xs text-muted-foreground">{t.role}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="border-t border-border py-20">
        <div className="container">
          <div className="rounded-2xl gradient-brand px-8 py-16 text-center">
            <h2 className="text-3xl font-semibold tracking-tight text-white sm:text-4xl">
              Your health record deserves better than a filing cabinet.
            </h2>
            <p className="mx-auto mt-4 max-w-xl text-white/90">
              Join HealthVault AI free and turn your first upload into a structured timeline in minutes.
            </p>
            <Link href="/register">
              <Button size="lg" variant="secondary" className="mt-8">
                Get started free
                <ArrowRight className="h-4 w-4" />
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-border py-12">
        <div className="container flex flex-col items-center justify-between gap-6 sm:flex-row">
          <div className="flex items-center gap-2">
            <span className="flex h-7 w-7 items-center justify-center rounded-lg gradient-brand">
              <ShieldCheck className="h-3.5 w-3.5 text-white" />
            </span>
            <span className="text-sm font-semibold">HealthVault AI</span>
          </div>
          <nav className="flex flex-wrap items-center justify-center gap-6 text-sm text-muted-foreground">
            <a href="#features" className="hover:text-foreground">Features</a>
            <a href="#pricing" className="hover:text-foreground">Pricing</a>
            <Link href="/dashboard" className="hover:text-foreground">Dashboard</Link>
            <a href="#" className="hover:text-foreground">Privacy</a>
            <a href="#" className="hover:text-foreground">Terms</a>
          </nav>
          <p className="text-xs text-muted-foreground">© 2026 HealthVault AI. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}
