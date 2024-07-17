'use client'

import { useState } from 'react'
import { useForm, SubmitHandler } from 'react-hook-form'
import  toast, { Toaster } from 'react-hot-toast'
import {
    Button,
    FormErrorMessage,
    FormLabel,
    FormControl,
    Text,
    Textarea,
    Box,
    Flex,
    Modal,
    ModalOverlay,
    ModalContent,
    ModalHeader,
    ModalFooter,
    ModalBody,
    ModalCloseButton,
} from '@chakra-ui/react'
import React from 'react'

export default function CommentModal({ isOpen, onClose, post_id }) {
    const [text, setText] = useState('')

    const {
        register,
        handleSubmit,
        formState: { errors, isSubmitting },
    } = useForm()

    const [submitError, setSubmitError] = useState(null)
    const notify = () => toast.success('Successfully commented!')

    const submitReply = async (value) => {
        const endpointUrl= await process.env.NEXT_PUBLIC_BACKEND_ENDPOINT_URL
        const res = await fetch(`${endpointUrl}/reply/${post_id}`, {
        method: "POST",
        credentials: "include",
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: value.text }),
        });

        if (!res.ok) {
            const data = await res.json();
            console.log(data)
            setSubmitError(data.detail);
        } else {
            onClose();
            const data = await res.json();
            console.log(data.message);
            notify();
        }
    };

    return (
        <>
        <Modal isOpen={isOpen} onClose={onClose} size={{ base: 'lg', xs: 'xs' }}>
            <ModalOverlay />
            <ModalContent>
            <ModalHeader>コメントする</ModalHeader>
            <ModalCloseButton />
            <ModalBody>
                <form onSubmit={handleSubmit(submitReply)}>
                <FormControl isInvalid={!!errors.text}>
                    <FormLabel>テキスト：</FormLabel>
                    <Textarea
                    {...register('text', {
                        required: 'テキストを入力してください．',
                        maxLength:{
                            value: 100,
                            message: "コメントは200文字以下で入力してください．"
                        },
                    })}
                    />
                    <FormErrorMessage>{errors.text?.message}</FormErrorMessage>
                </FormControl>
                {submitError && (
                    <Text color="red.500" mt={2}>
                    {submitError}
                    </Text>
                )}
                <Flex justify="flex-end" mt={4}>
                    <Button size="lg" colorScheme="blue" type="submit" isLoading={isSubmitting}>
                    コメントする
                    </Button>
                </Flex>
                </form>
            </ModalBody>
            <ModalFooter/>
            </ModalContent>
        </Modal>
        <Toaster />
        </>
    )
}
