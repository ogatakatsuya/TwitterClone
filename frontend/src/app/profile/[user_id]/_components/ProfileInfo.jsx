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

const ProfileInfo = () => {
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
        const res = await fetch(`${endpointUrl}/profile`, {
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
        const res = await fetch(`${endpointUrl}/profile`,{
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

    if (!profile) {
        return <Text>Loading...</Text>;
    }

    return (
        <>
            <Grid templateColumns="1fr 400px" gap={50} padding={4} bgColor="gray.50">
                <Container centerContent>
                    <Avatar size="2xl" src={profile?.avatar_url} />
                    <Text mt={1} as="b">
                        {profile?.nickname}
                    </Text>
                    <Text as="i" opacity="0.5">
                        @{profile?.name}
                    </Text>
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
                        <Text>{profile?.birth_day ? `Birthday : ${profile.birth_day}` : "Birthday : Tell me your birthday!"}</Text>
                        <Button bgColor="blue.200" onClick={onOpen}>
                            Edit Profile
                        </Button>
                    </Stack>
                </Flex>
            </Grid>
            <Modal
                isOpen={isOpen}
                onClose={onClose}
            >
                <ModalOverlay />
                <ModalContent>
                <ModalHeader>Edit your profile</ModalHeader>
                <ModalCloseButton />
                <ModalBody pb={6}>
                    <form onSubmit={handleSubmit(editHandler)}>
                        <FormControl>
                        <FormLabel>Nickname</FormLabel>
                        <Input placeholder='Nick Name' {
                            ...register("nickname")
                        } 
                        default={profile.nickname}/>
                        </FormControl>

                        <FormControl mt={4}>
                        <FormLabel>Birthday</FormLabel>
                        <Input placeholder='Birthday' type="date" {
                            ...register("birthday")
                        } 
                        default={profile.birth_day}/>
                        </FormControl>

                        <FormControl mt={4}>
                        <FormLabel>Biography</FormLabel>
                        <Textarea placeholder='Biography' {
                            ...register("biography")
                        }
                        default={profile.biography}/>
                        </FormControl>
                        <Flex justifyContent="end">
                            <Button colorScheme='blue' mr={3} type="submit" isLoading={isSubmitting} mt={4}>
                                Edit
                            </Button>
                            <Button onClick={onClose} mt={4}>Cancel</Button>
                        </Flex>
                    </form>
                </ModalBody>
                </ModalContent>
            </Modal>
        </>
    );
};

export default ProfileInfo;
