'use client'

import { useState, FormEvent, ChangeEvent } from 'react'
import { useRouter } from 'next/navigation'

export default function SearchBar(){
    const [query, setQuery] = useState('')
    const [suggestions, setSuggestions] = useState([])
    
    const router = useRouter()

    const handleSearch = (e: FormEvent<HTMLFormElement>) =>{
        e.preventDefault();
        router.push(`/products?q=${encodeURIComponent(query)}`)
    }

    const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
        setQuery(e.target.value)
    }

    async function fetchSuggestions(searchText: string) {
        if (searchText.trim() === '') {
            setSuggestions([]);
            return;
        }
        const res = await fetch(`http://localhost:8000/api/products/search/?query=${encodeURIComponent(searchText)}`);
        const data = await res.json();
        setSuggestions(data);
    }

    return(
        <form 
          onSubmit={handleSearch} 
        >
            <div className="dropdown">
                <input 
                    tabIndex={0} 
                    className="input border" 
                    id="part" 
                    type="text"
                    name="part" 
                    value={query}
                    placeholder='Rtx 3070...'
                    onChange={handleChange} 
                />
                <ul tabIndex={0} id='suggestions' className="dropdown-content menu bg-base-100 rounded-box z-1 w-52 p-2 shadow-sm">
                    <li><a>Item 1</a></li>
                    <li><a>Item 2</a></li>
                </ul>
            </div>
        <button type="submit"className="btn ms-2">Search</button>
        </form>
    )
}