"use client";

import {
    Avatar,
    Text,
    Grid,
    Button,
    Flex,
    Container,
    useDisclosure,
    Stack,
    Card,
    CardBody,
    HStack,
} from "@chakra-ui/react";
import { useEffect, useState } from "react";
import MyFollow from "./MyFollow";
import MyFollower from "./MyFollower";
import FileUploadButton from "./FileUploadButton";
import ProfileModal from "./ProfileModal";

const MyProfileInfo = () => {
    const [profile, setProfile] = useState(null);
    const { isOpen, onOpen, onClose } = useDisclosure();

    const fetchProfile = async () => {
        const endpointUrl = process.env.NEXT_PUBLIC_BACKEND_ENDPOINT_URL;
        const res = await fetch(`${endpointUrl}/profile`, {
            method: "GET",
            credentials: "include",
        });
        if (res.ok) {
            const data = await res.json();
            setProfile(data);
        }
    };

    useEffect(() => {
        fetchProfile();
    }, []);

    const formatDate = (date) => {
        const year = date.getFullYear();
        const month = (`0${date.getMonth() + 1}`).slice(-2);
        const day = (`0${date.getDate()}`).slice(-2);
        return `${year}/${month}/${day}`;
    };

    if (!profile) {
        return <Text>Loading...</Text>;
    }

    return (
        <>
            <Grid templateColumns="1fr 400px" gap={50} padding={4} bgColor="gray.50">
                <Container centerContent>
                    <Avatar size="2xl" src={profile?.icon_url} />
                    <Text mt={1} as="b">
                        {profile?.nickname}
                    </Text>
                    <Text as="i" opacity="0.5">
                        @{profile?.name}
                    </Text>
                    <HStack>
                        <MyFollow />
                        <MyFollower />
                    </HStack>
                </Container>
                <Flex alignItems="center" justifyContent="center">
                    <Stack spacing={4} textAlign="center">
                    <Card maxHeight="150px" overflowY="auto">
                        <CardBody>
                            <Text as="b">
                                {profile?.biography ? profile.biography : "Biography : Tell me about yourself!"}
                            </Text>
                        </CardBody>
                    </Card>
                        <Text as="b">{profile?.birth_day ? `Birthday : ${formatDate(new Date(profile.birth_day))}` : "Birthday : Tell me your birthday!"}</Text>
                        <Button bgColor="blue.200" onClick={onOpen}>
                            Edit Profile
                        </Button>
                        <FileUploadButton />
                    </Stack>
                </Flex>
            </Grid>
            <ProfileModal isOpen={isOpen} onClose={onClose} profile={profile} fetchProfile={fetchProfile}/>
        </>
    );
};

export default MyProfileInfo;
