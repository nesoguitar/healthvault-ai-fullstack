"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { HeartPulse, TrendingUp } from "lucide-react";
import { HealthScoreBreakdown } from "@/types";

export function HealthScoreCard({ healthScore }: { healthScore: HealthScoreBreakdown }) {
  const { overall, categories } = healthScore;
  const circumference = 2 * Math.PI * 42;
  const offset = circumference - (overall / 100) * circumference;

  return (
    <Card className="lg:col-span-2">
      <CardHeader className="flex-row items-center justify-between space-y-0">
        <CardTitle className="text-base">Health Score</CardTitle>
        <span className="flex items-center gap-1 text-xs font-medium text-success">
          <TrendingUp className="h-3.5 w-3.5" />
          Trending well
        </span>
      </CardHeader>
      <CardContent>
        <div className="flex flex-col items-center gap-6 sm:flex-row">
          <div className="relative h-32 w-32 shrink-0">
            <svg viewBox="0 0 100 100" className="h-full w-full -rotate-90">
              <circle cx="50" cy="50" r="42" fill="none" stroke="hsl(var(--muted))" strokeWidth="10" />
              <circle
                cx="50"
                cy="50"
                r="42"
                fill="none"
                stroke="url(#scoreGradient)"
                strokeWidth="10"
                strokeLinecap="round"
                strokeDasharray={circumference}
                strokeDashoffset={offset}
              />
              <defs>
                <linearGradient id="scoreGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stopColor="hsl(217 91% 45%)" />
                  <stop offset="100%" stopColor="hsl(174 72% 36%)" />
                </linearGradient>
              </defs>
            </svg>
            <div className="absolute inset-0 flex flex-col items-center justify-center">
              <HeartPulse className="h-4 w-4 text-teal" />
              <span className="text-2xl font-semibold">{overall}</span>
            </div>
          </div>

          <div className="w-full flex-1 space-y-3">
            {categories.map((c) => (
              <div key={c.label}>
                <div className="mb-1 flex items-center justify-between text-xs">
                  <span className="text-muted-foreground">{c.label}</span>
                  <span className="font-medium">{c.score}</span>
                </div>
                <div className="h-1.5 w-full overflow-hidden rounded-full bg-muted">
                  <div className="h-full gradient-brand rounded-full" style={{ width: `${c.score}%` }} />
                </div>
              </div>
            ))}
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
