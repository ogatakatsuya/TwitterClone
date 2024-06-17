"use client";

import { HStack, Text } from "@chakra-ui/react";
import { useState, useEffect } from "react";

const Follow = () => {
    const [ followNum, setFollowNum ] = useState(0);
    useEffect(() => {
        fetchFollowNum()
    })
    const fetchFollowNum = async() => {
        const endpointUrl = process.env.NEXT_PUBLIC_BACKEND_ENDPOINT_URL
        const res = await fetch(`${endpointUrl}/follow`,{
            method: "GET",
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: "include",
        })
        if(res.ok){
            const data = await res.json();
            setFollowNum(data)
        } else {
            console.log('error');
        }
    }
    return (
        <>
            <HStack>
                <Text as="b">{followNum}</Text>
                <Text opacity={0.5}>Following</Text>
            </HStack>
        </>
    )
}

export default Follow;