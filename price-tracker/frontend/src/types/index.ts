export interface Website{
    id: number;
    name: string;
}

export interface Product{
    id: string;
    website: Website;
    category: string;
    name: string;
    short_description: string;
    url: string;
    image_url: string;
    price: string;
    availability: boolean
}