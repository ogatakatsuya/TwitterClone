'use client'

import { useState } from 'react'
import { useForm, SubmitHandler } from 'react-hook-form'
import {
    Button,
    FormErrorMessage,
    FormLabel,
    Heading,
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

export default function CommentModal({ isOpen, onOpen, onClose }) {
const [text, setText] = useState('')

const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
} = useForm()

const [submitError, setSubmitError] = useState(null)

return (
    <>
    <Modal isOpen={isOpen} onClose={onClose} size={{ base: 'lg', xs: 'xs' }}>
        <ModalOverlay />
        <ModalContent>
        <ModalHeader>コメントする</ModalHeader>
        <ModalCloseButton />
        <ModalBody>
            <form >
            <FormControl isInvalid={!!errors.text}>
                <FormLabel>テキスト：</FormLabel>
                <Textarea
                {...register('text', {
                    required: 'テキストを入力してください．',
                })}
                />
                <FormErrorMessage>{errors.text && errors.text.message}</FormErrorMessage>
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
        <ModalFooter></ModalFooter>
        </ModalContent>
    </Modal>
    </>
)
}
