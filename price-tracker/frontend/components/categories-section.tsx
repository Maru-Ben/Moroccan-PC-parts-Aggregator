"use client"

import { Card, CardContent } from "@/components/ui/card"
import { useLanguage } from "@/contexts/language-context"
import { ChevronLeft, ChevronRight } from "lucide-react"
import { useRef, useState } from "react"
import { Button } from "@/components/ui/button"
import Link from "next/link"

const getCategoryData = (t: any) => [
  {
    name: t.processors,
    value: "processors",
    count: `250+ ${t.products}`,
    image: "/gaming-cpu-processor-dark-cyan-lighting.jpg",
  },
  {
    name: t.graphicsCards,
    value: "graphics-cards",
    count: `180+ ${t.products}`,
    image: "/gaming-gpu-graphics-card-dark-rgb.jpg",
  },
  {
    name: t.memory,
    value: "memory",
    count: `320+ ${t.products}`,
    image: "/gaming-ram-memory-dark-cyan-rgb.jpg",
  },
  {
    name: t.storage,
    value: "storage",
    count: `400+ ${t.products}`,
    image: "/gaming-nvme-ssd-dark-blue-lighting.jpg",
  },
  {
    name: t.motherboards,
    value: "motherboards",
    count: `150+ ${t.products}`,
    image: "/gaming-motherboard-dark-cyan-circuits.jpg",
  },
  {
    name: t.powerSupply,
    value: "power-supply",
    count: `120+ ${t.products}`,
    image: "/gaming-psu-power-supply-dark-blue.jpg",
  },
]

export function CategoriesSection() {
  const { t } = useLanguage()
  const categories = getCategoryData(t)
  const scrollContainerRef = useRef<HTMLDivElement>(null)
  const [canScrollLeft, setCanScrollLeft] = useState(false)
  const [canScrollRight, setCanScrollRight] = useState(true)

  const scroll = (direction: "left" | "right") => {
    if (scrollContainerRef.current) {
      const scrollAmount = 300
      const newScrollLeft =
        scrollContainerRef.current.scrollLeft + (direction === "left" ? -scrollAmount : scrollAmount)
      scrollContainerRef.current.scrollTo({
        left: newScrollLeft,
        behavior: "smooth",
      })
    }
  }

  const checkScrollButtons = () => {
    if (scrollContainerRef.current) {
      const { scrollLeft, scrollWidth, clientWidth } = scrollContainerRef.current
      setCanScrollLeft(scrollLeft > 0)
      setCanScrollRight(scrollLeft < scrollWidth - clientWidth - 10)
    }
  }

  return (
    <section className="py-16 lg:py-24 bg-background relative overflow-hidden">
      <div className="absolute inset-0 opacity-5">
        <div className="absolute top-10 left-10 w-2 h-2 bg-primary rounded-full animate-pulse"></div>
        <div className="absolute top-32 right-20 w-1 h-1 bg-primary rounded-full animate-pulse delay-1000"></div>
        <div className="absolute bottom-20 left-1/4 w-1.5 h-1.5 bg-primary rounded-full animate-pulse delay-500"></div>
        <div className="absolute bottom-40 right-1/3 w-1 h-1 bg-primary rounded-full animate-pulse delay-1500"></div>
      </div>

      <div className="container mx-auto px-4 relative z-10">
        <div className="mb-12 text-center">
          <h2 className="mb-4 text-3xl font-bold tracking-tight lg:text-4xl text-foreground">{t.shopByCategory}</h2>
          <p className="text-lg text-muted-foreground">{t.categoryDescription}</p>
        </div>

        {/* Horizontal scroll container with buttons */}
        <div className="relative max-w-6xl mx-auto">
          <Button
            variant="outline"
            size="lg"
            className={`absolute -left-16 top-1/2 -translate-y-1/2 z-20 bg-cyan-500/20 backdrop-blur-sm border-2 border-cyan-400 hover:bg-cyan-500/30 hover:border-cyan-300 hover:shadow-[0_0_20px_rgba(0,200,255,0.5)] transition-all w-14 h-14 rounded-2xl opacity-70 ${
              !canScrollLeft ? "opacity-50 cursor-not-allowed" : ""
            }`}
            onClick={() => scroll("left")}
            disabled={!canScrollLeft}
          >
            <ChevronLeft className="h-6 w-6 text-cyan-300" />
          </Button>

          <div
            ref={scrollContainerRef}
            onScroll={checkScrollButtons}
            className="overflow-x-auto scroll-smooth pb-4 custom-scrollbar"
          >
            <div className="flex gap-4 md:gap-6 min-w-max px-2">
              {categories.map((category, index) => (
                <div key={index} className="w-64 md:w-72 flex-shrink-0">
                  <Link href={`/search?category=${category.value}`}>
                    <Card className="gaming-card group cursor-pointer transition-all duration-300 hover:scale-105 h-full">
                      <CardContent className="p-0">
                        <div className="relative overflow-hidden rounded-t-lg">
                          <img
                            src={category.image || "/placeholder.svg"}
                            alt={category.name}
                            className="w-full h-48 object-cover transition-transform duration-300 group-hover:scale-110"
                          />
                          <div className="absolute inset-0 bg-gradient-to-t from-background/80 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
                        </div>
                        <div className="p-6 text-center">
                          <h3 className="mb-2 font-semibold text-balance text-foreground group-hover:text-primary transition-colors duration-300">
                            {category.name}
                          </h3>
                          <p className="text-sm text-muted-foreground">{category.count}</p>
                        </div>
                      </CardContent>
                    </Card>
                  </Link>
                </div>
              ))}
            </div>
          </div>

          <Button
            variant="outline"
            size="lg"
            className={`absolute -right-16 top-1/2 -translate-y-1/2 z-20 h-14 bg-cyan-500/20 backdrop-blur-sm border-2 border-cyan-400 hover:bg-cyan-500/30 hover:border-cyan-300 hover:shadow-[0_0_20px_rgba(0,200,255,0.5)] transition-all w-14 rounded-2xl opacity-70 ${
              !canScrollRight ? "opacity-50 cursor-not-allowed" : ""
            }`}
            onClick={() => scroll("right")}
            disabled={!canScrollRight}
          >
            <ChevronRight className="h-6 w-6 text-cyan-300" />
          </Button>
        </div>
      </div>
    </section>
  )
}
