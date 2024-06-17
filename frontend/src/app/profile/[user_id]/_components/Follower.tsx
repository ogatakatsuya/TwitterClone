"use client";

import { HStack, Text } from "@chakra-ui/react";
import { useState, useEffect } from "react";

const Follower = ({user_id}) => {
    const [ followerNum, setFollowerNum ] = useState(0);
    useEffect(() => {
        fetchFollowerNum()
    })
    const fetchFollowerNum = async() => {
        const endpointUrl = process.env.NEXT_PUBLIC_BACKEND_ENDPOINT_URL
        const res = await fetch(`${endpointUrl}/followed/${user_id}`,{
            method: "GET",
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: "include",
        })
        if(res.ok){
            const data = await res.json();
            setFollowerNum(data)
        } else {
            console.log('error');
        }
    }
    return (
        <>
            <HStack>
                <Text as="b">{followerNum}</Text>
                <Text opacity={0.5}>Follower</Text>
            </HStack>
        </>
    )
}

export default Follower;