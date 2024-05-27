"use client";
import { Heading } from "@chakra-ui/react"
import { useEffect, useState } from "react";

export default function Home() {
  const [ data, setData ] = useState(""); 
  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await fetch('http://localhost:8000/hello', {
          method: 'GET',
        })
        if (res.ok) {
          const data = await res.json()
          setData(data.message)
        } else {
          console.error('Error fetching tasks:', res.statusText)
        }
      } catch (error) {
        console.error('Error fetching tasks:', error)
      }
    }
    fetchData()
  }, [])
  return (
    <Heading>{data}</Heading>
  );
}
