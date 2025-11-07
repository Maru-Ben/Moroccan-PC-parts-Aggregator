"use client"

import { Wrench, ArrowRight, Star } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { useLanguage } from "@/contexts/language-context"

export function BuildPcSection() {
  const { t, isRTL } = useLanguage()

  return (
    <section className="py-16 lg:py-24 bg-muted/30">
      <div className="container mx-auto px-4">
        <div className="mx-auto max-w-4xl">
          <Card className="overflow-hidden bg-border py-8">
            <CardContent className="p-6 py-0">
              <div className="grid lg:grid-cols-2">
                {/* Content */}
                <div className="p-8 lg:p-12 lg:py-3 lg:px-5">
                  <div className="mb-4">
                    <Badge variant="secondary" className="mb-4">
                      {t.comingSoon}
                    </Badge>
                    <div className={`flex items-center gap-2 mb-4 ${isRTL ? "flex-row-reverse" : ""}`}>
                      <Wrench className="h-6 w-6 text-accent" />
                      <h2 className="text-2xl font-bold lg:text-3xl">{t.buildYourPc}</h2>
                    </div>
                  </div>

                  <p className="mb-6 text-muted-foreground text-pretty">{t.buildDescription}</p>

                  <div className="mb-8 space-y-3">
                    <div className={`flex items-center gap-3 ${isRTL ? "flex-row-reverse" : ""}`}>
                      <Star className="h-4 w-4 text-accent" />
                      <span className="text-sm">{t.compatibilityChecking}</span>
                    </div>
                    <div className={`flex items-center gap-3 ${isRTL ? "flex-row-reverse" : ""}`}>
                      <Star className="h-4 w-4 text-accent" />
                      <span className="text-sm">{t.budgetOptimization}</span>
                    </div>
                    <div className={`flex items-center gap-3 ${isRTL ? "flex-row-reverse" : ""}`}>
                      <Star className="h-4 w-4 text-accent" />
                      <span className="text-sm">{t.performanceBenchmarks}</span>
                    </div>
                  </div>

                  <Button disabled className="group">
                    {t.getNotified}
                    <ArrowRight
                      className={`h-4 w-4 transition-transform group-hover:translate-x-1 ${isRTL ? "ml-2 group-hover:-translate-x-1" : "ml-2"}`}
                    />
                  </Button>
                </div>

                {/* Visual */}
                <div className="bg-gradient-to-br from-accent/10 to-accent/5 p-8 lg:p-12">
                  <div className="flex h-full items-center justify-center">
                    <div className="text-center">
                      <div className="mx-auto mb-6 grid h-32 w-32 place-items-center rounded-2xl bg-accent/10">
                        <Wrench className="h-16 w-16 text-accent" />
                      </div>
                      <p className="text-sm text-muted-foreground">Advanced PC building tools</p>
                    </div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </section>
  )
}
