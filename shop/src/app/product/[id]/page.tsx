// src/app/product/[id]/page.tsx
import React from 'react';
import Image from 'next/image';

type Props = {
  params: Promise<{ id: string }>;
};

/* ── 1.  tell Next.js which urls to pre-render ------------------------------ */
export async function generateStaticParams() {
  // replace with your real slugs / ids
  return [
    { id: 'blue-vase' },
    { id: 'red-mug' },
    { id: 'yellow-bowl' },
  ];
}

/* ── 2.  page component ----------------------------------------------------- */
export default function Product({ params }: Props) {
  const { id } = React.use(params); // unwrap promise

  const data = {
    title: 'Blue Pottery Vase',
    story: 'Hand-made in Jaipur...',
    price: 350,
    images: [
      'https://placehold.co/600x400',
      'https://placehold.co/600x400',
      'https://placehold.co/600x400',
      'https://placehold.co/600x400',
    ],
  };

  return (
    <main className="p-4 max-w-4xl mx-auto">
      <div className="grid grid-cols-2 gap-4">
        {data.images.map((src, i) => (
          <Image
            key={i}
            src={src}
            width={600}
            height={400}
            className="rounded"
            alt={`Product image ${i + 1}`}
          />
        ))}
      </div>

      <h2 className="text-2xl mt-4">{data.title}</h2>
      <p className="mt-2 text-gray-700">{data.story}</p>
      <p className="mt-4 text-xl font-semibold">₹{data.price}</p>

      <button className="mt-4 bg-green-500 text-white px-6 py-2 rounded">
        Pay with UPI
      </button>
    </main>
  );
}
