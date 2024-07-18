"use client";

import { useState, useEffect } from "react"
import { IconButton, Text } from "@chakra-ui/react"

import { BiLike } from "react-icons/bi";
import { BiSolidLike } from "react-icons/bi";

const LikeButton = ({ post_id }) => {
    const [likeNum, setLikeNum] = useState(0);
    const [pushed, setPushed] = useState(false);
    const endpointUrl = process.env.NEXT_PUBLIC_BACKEND_ENDPOINT_URL
    
    const handleLike = () => {
        const method = pushed ? 'DELETE' : 'POST';
        handleLikeRequest(method);
        setPushed(!pushed);
    };

    const handleLikeRequest = async (method) => {
        const res = await fetch(`${endpointUrl}/like/${post_id}`, {
            method: method,
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (res.ok) {
            const data = await res.json();
            setLikeNum(prev => prev + (method === 'POST' ? 1 : -1));
        } else {
            console.error('Error:');
        }
    };

    useEffect(() => {
        fetchLikeNum();
    }, []);

    const fetchLikeNum = async () => {
        try {
            const res = await fetch(`${endpointUrl}/likes/${post_id}`, {
                method: "GET",
                credentials: "include",
            });
            if (res.ok) {
                const data = await res.json();
                setLikeNum(data.like_num);
                setPushed(data.is_like);
            } else {
                console.error("Error fetching like:", res.statusText);
            }
        } catch (error) {
            console.error("Error fetching like:", error);
        }
    };

    return (
        <>
            <Text mb={1} mr={1}>{likeNum}</Text>
            <IconButton 
                icon={pushed ? <BiSolidLike /> : <BiLike />} 
                onClick={handleLike}
                aria-label="Like button"
                mr="4"
                size="sm"
            />
        </>
    );
}

export default LikeButton;
