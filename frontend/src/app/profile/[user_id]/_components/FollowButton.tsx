"use client";

import { Button } from "@chakra-ui/react";
import { useState, useEffect } from "react";

const FollowButton = ({ user_id }) => {
    const [ following, setFollowing ] = useState(false);
    const endpointUrl = process.env.NEXT_PUBLIC_BACKEND_ENDPOINT_URL;

    useEffect(() => {
        isLike()
    },[])

    const isLike = async () => {
        const res = await fetch(`${endpointUrl}/isfollow/${user_id}`,{
            method: "GET",
            credentials: "include"
        })
        const data = await res.json()
        setFollowing(data)
    }

    const clickHandler = () => {
        const method = following ? "DELETE" : "POST";
        followHandler(method);
        setFollowing(!following);
    }

    const followHandler = async (method) => {
        const res = await fetch(`${endpointUrl}/follow/${user_id}`,{
            method : method,
            credentials: "include",
            headers: {
                'Content-Type': 'application/json',
            },
        })
        if (res.ok) {
            const data = await res.json();
        } else {
            console.log('error');
        }
    };
    return (
        <> 
            {following ? (
                <Button onClick={clickHandler}>
                    Following
                </Button>
            ):
                <Button onClick={clickHandler}>
                    Follow
                </Button>
            }
        </>
    )
}

export default FollowButton;