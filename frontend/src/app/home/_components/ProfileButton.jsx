"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@chakra-ui/react";

const ProfileButton = () => {
    const [userId, setUserId] = useState("");
    const router = useRouter();
    const endpointUrl = process.env.NEXT_PUBLIC_BACKEND_ENDPOINT_URL;
    const fetchUserId = async () => {
        try {
            const res = await fetch(`${endpointUrl}/user`, {
                method: "GET",
                credentials: "include",
            });
            if (res.ok) {
                const data = await res.json();
                setUserId(data);
            } else {
            }
        } catch (error) {
        } 
    };
    useEffect(() => {
        fetchUserId();
    }, []);

    const redirectToProfile = () => {
        router.push(`/profile/${userId}`)
    }

    return (
        <Button variant="link" onClick={redirectToProfile}>Profile</Button>
    );
};

export default ProfileButton;
