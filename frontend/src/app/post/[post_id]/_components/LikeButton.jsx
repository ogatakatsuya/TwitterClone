"use client";

import { useState, useEffect} from "react"
import { IconButton, Text } from "@chakra-ui/react"

import { BiLike } from "react-icons/bi";
import { BiSolidLike } from "react-icons/bi";

const LikeButton = ({ post_id }) => {
    const [ pushed, setPushed ] = useState(false);
    const [ likeNum, setLikeNum ] = useState();
    const endpointUrl= process.env.NEXT_PUBLIC_BACKEND_ENDPOINT_URL
    
    const handleLike = () => {
        if (!pushed){
            createLike()
        } else {
            deleteLike()
        }
        setPushed((prev) => !prev)
    };

    const createLike = async () => {
        const res = await fetch(`${endpointUrl}/like/${post_id}`,{
            method: "POST",
            credentials: "include",
            headers: {
                'Content-Type': 'application/json',
            }
        });
        if(res.ok){
            const data = await res.json();
            console.log(data)
            setLikeNum((prev) => prev+1)
        }else{
            console.log("error");
        }
    }

    const deleteLike = async () => {
        const res = await fetch(`${endpointUrl}/like/${post_id}`,{
            method: "DELETE",
            credentials: "include",
            headers: {
                'Content-Type': 'application/json',
            }
        });
        if(res.ok){
            const data = await res.json();
            console.log(data)
            setLikeNum((prev) => prev-1)
        }else{
            console.log("error");
        }
    }

    
    useEffect(() => {
        fetchLikeNum()
    },[])

    const fetchLikeNum = async () => {
        try {
            const res = await fetch(`${endpointUrl}/likes/${post_id}`, {
                method: "GET",
            });
            if (res.ok) {
                const data = await res.json();
                setLikeNum(data.like_num);
                console.log(data);
            } else {
                console.error("Error fetching like:", res.statusText);
            }
        } catch (error) {
            console.error("Error fetching like:", error);
        }
    }
    return (
        <>
        <Text mb={1} mr={1}>{likeNum}</Text>
        <IconButton 
            icon={pushed ? <BiSolidLike /> : <BiLike />} 
            onClick={() => handleLike()}
            aria-label="Like button"
            mr="4"
            size="sm"
        />
        </>
    )
}

export default LikeButton;

