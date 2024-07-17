"use client";

import { useForm, SubmitHandler } from "react-hook-form"
import toast, { Toaster } from "react-hot-toast";
import {
    Modal,
    ModalOverlay,
    ModalContent,
    ModalHeader,
    ModalCloseButton,
    ModalBody,
    FormControl,
    FormLabel,
    Input,
    FormErrorMessage,
    Textarea,
    Flex,
    Button,
} from "@chakra-ui/react";

const ProfileModal = ({isOpen,onClose,profile, fetchProfile}) => {
    const {
        register,
        handleSubmit,
        watch,
        formState: { errors, isSubmitting },
    } = useForm()

    const editHandler = async (value) => {
        const notify = () => toast.success("Profile updated successfully");
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
            notify();
        } else {
            console.log("error");
        }
    }
    return(
        <>
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
                            ...register("nickname",{
                                required: "Nickname is required",
                            })
                        } 
                        defaultValue={profile.nickname}/>
                        </FormControl>

                        <FormControl mt={4}>
                        <FormLabel>Birthday</FormLabel>
                        <Input placeholder='Birthday' type="date" {
                            ...register("birthday",{
                                required: "Birthday is required",
                            })
                        } 
                        defaultValue={profile.birth_day}/>
                        </FormControl>

                        <FormControl mt={4}>
                        <FormLabel>Biography</FormLabel>
                        <Textarea placeholder='Biography' {
                            ...register("biography",{
                                required: "Biography is required",
                            })
                        }
                        defaultValue={profile.biography}/>
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
            <Toaster />
        </>
    )
}

export default ProfileModal;