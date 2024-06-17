"use client";

import {
    Avatar,
    Text,
    Grid,
    Button,
    Flex,
    Box,
    Container,
    useDisclosure,
    Modal,
    ModalOverlay,
    ModalContent,
    ModalHeader,
    ModalFooter,
    ModalBody,
    ModalCloseButton,
    FormControl,
    FormLabel,
    Input,
    Textarea,
    Stack,
    Card,
    CardBody
} from "@chakra-ui/react";

import { useEffect, useState } from "react";
import { useForm, SubmitHandler } from "react-hook-form"
import { LiaBirthdayCakeSolid } from "react-icons/lia";

const ProfileInfo = ({ user_id }) => {
    const [profile, setProfile] = useState(null);
    const { isOpen, onOpen, onClose } = useDisclosure();
    const {
        register,
        handleSubmit,
        watch,
        formState: { errors, isSubmitting },
    } = useForm()

    const fetchProfile = async () => {
        const endpointUrl = process.env.NEXT_PUBLIC_BACKEND_ENDPOINT_URL;
        const res = await fetch(`${endpointUrl}/profile/${user_id}`, {
            method: "GET",
            credentials: "include",
        });
        if (res.ok) {
            const data = await res.json();
            console.log(data);
            setProfile(data);
        }
    };

    useEffect(() => {
        fetchProfile();
    }, []);

    const editHandler = async (value) => {
        const endpointUrl = process.env.NEXT_PUBLIC_BACKEND_ENDPOINT_URL;
        const res = await fetch(`${endpointUrl}/profile/${user_id}`,{
            method: "PUT",
            credentials: "include",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                nickname: value.nickname,
                biography: value.biography,
                birth_day: value.birthday
            })
        })
        if(res.ok){
            onClose();
            fetchProfile();
        } else {
            console.log("error");
        }
    }

    const formatDate = (date) => {
        const year = date.getFullYear();
        const month = ('0' + (date.getMonth() + 1)).slice(-2);
        const day = ('0' + date.getDate()).slice(-2);
        return `${year}/${month}/${day}`;
    };

    if (!profile) {
        return <Text>Loading...</Text>;
    }

    return (
        <>
            <Grid templateColumns="1fr 400px" gap={50} padding={4} bgColor="gray.50">
                <Container centerContent>
                    <Avatar size="2xl" src={profile?.avatar_url} />
                    <Text mt={1} as="b">
                        {profile.nickname ? profile.nickname : "unknown"}
                    </Text>
                    <Text as="i" opacity="0.5">
                        @{profile.name}
                    </Text>
                </Container>
                <Flex alignItems="center" justifyContent="center">
                    <Stack spacing={4} textAlign="center">
                    <Card maxHeight="150px" overflowY="auto">
                        <CardBody>
                            <Text as="b">
                                {profile?.biography ? profile.biography : "Biography : unknown"}
                            </Text>
                        </CardBody>
                    </Card>
                        <Text as="b">{profile?.birth_day ? `Birthday : ${formatDate(new Date(profile.birth_day))}` : "Birthday : unknown"}</Text>
                    </Stack>
                </Flex>
            </Grid>
        </>
    );
};

export default ProfileInfo;
