"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@chakra-ui/react";

const ProfileButton = () => {
    const router = useRouter();

    const redirectToProfile = () => {
        router.push(`/profile/me`)
    }

    return (
        <Button variant="link" onClick={redirectToProfile}>Profile</Button>
    );
};

export default ProfileButton;
