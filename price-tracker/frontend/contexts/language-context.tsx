"use client"

import { createContext, useContext, useState, useEffect, type ReactNode } from "react"
import type { Language, Translations } from "@/lib/i18n"
import { getTranslation } from "@/lib/i18n"

interface LanguageContextType {
  language: Language
  setLanguage: (language: Language) => void
  t: Translations
  isRTL: boolean
}

const LanguageContext = createContext<LanguageContextType | undefined>(undefined)

export function LanguageProvider({ children }: { children: ReactNode }) {
  const [language, setLanguageState] = useState<Language>("en")
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    // Get language from localStorage or browser preference
    const savedLanguage = localStorage.getItem("language") as Language
    const browserLanguage = navigator.language.split("-")[0] as Language

    if (savedLanguage && ["en", "fr", "ar"].includes(savedLanguage)) {
      setLanguageState(savedLanguage)
    } else if (["en", "fr", "ar"].includes(browserLanguage)) {
      setLanguageState(browserLanguage)
    }

    setMounted(true)
  }, [])

  useEffect(() => {
    if (mounted) {
      localStorage.setItem("language", language)

      // Update document direction and language
      document.documentElement.lang = language
      document.documentElement.dir = language === "ar" ? "rtl" : "ltr"

      // Update body class for RTL styling
      if (language === "ar") {
        document.body.classList.add("rtl")
      } else {
        document.body.classList.remove("rtl")
      }
    }
  }, [language, mounted])

  const setLanguage = (newLanguage: Language) => {
    setLanguageState(newLanguage)
  }

  const t = getTranslation(language)
  const isRTL = language === "ar"

  if (!mounted) {
    return null
  }

  return <LanguageContext.Provider value={{ language, setLanguage, t, isRTL }}>{children}</LanguageContext.Provider>
}

export function useLanguage() {
  const context = useContext(LanguageContext)
  if (context === undefined) {
    throw new Error("useLanguage must be used within a LanguageProvider")
  }
  return context
}
