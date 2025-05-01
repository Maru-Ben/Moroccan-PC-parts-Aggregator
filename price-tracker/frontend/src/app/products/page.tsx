import { Product } from '@/types'

interface SearchParams{
    q: string;
}

export default async function ProductsPage({ searchParams }: {searchParams: SearchParams}){
    const query = searchParams.q;

    const res = await fetch(`http://localhost:8000/api/products/search/?query=${query}`);
    const products = await res.json()

    return (
        <>
            { products.length === 0 ? (
                <p>No products Found</p>
            ) : (
                <ul className="space-y-4">
                {products.map((product: Product) => (
                    <li
                    key={product.id}
                    className="border p-4 rounded-lg shadow-lg hover:shadow-xl transition-all"
                    >
                        <h3 className="text-xl font-semibold">{product.name}</h3>
                        <p className="text-gray-600">{product.price} dh</p>
                    </li>
                ))}
                </ul>
            )}
        </>
    )
}