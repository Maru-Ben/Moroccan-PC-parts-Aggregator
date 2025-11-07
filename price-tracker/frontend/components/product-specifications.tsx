import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

interface Specification {
  label: string
  value: string
}

interface ProductSpecificationsProps {
  specifications: Specification[]
}

export function ProductSpecifications({ specifications }: ProductSpecificationsProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Specifications</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="grid gap-3">
          {specifications.map((spec, index) => (
            <div key={index} className="flex justify-between py-2 border-b border-border last:border-b-0">
              <span className="font-medium text-muted-foreground">{spec.label}</span>
              <span className="text-right font-mono text-sm">{spec.value}</span>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}
