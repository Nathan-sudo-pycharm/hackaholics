
import PatientForm from '@/components/forms/PatientForm'

import Image from 'next/image'
import Link from 'next/link'
import React from 'react'

export default function page() {
  return (
    <div className='flex h-screen max-h-screen'>
      <section className='remove-scrollbar container my-auto'>
        <div className='sub-container max-w-[496px]'>
          
        <PatientForm/>
        <div className='text-14-regular mt-20 flex justify-between'>
          <p className='justify-items-end text-dark-600 xl:text-left'>
        © 2024 MediSafe
        </p>
        <Link href="/?admin=true" className="text-green-500">Admin</Link>
        </div>
        </div>

      </section>
      <Image
      src="/public/images/oghealth.png"
      height={4000}
      width={4000}
      alt="patient"
      />

      </div>
  )
}