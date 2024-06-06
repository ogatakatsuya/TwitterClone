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

export default function PostModal({ isOpen, onOpen, onClose }) {
  const [text, setText] = useState('')

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm()

  const [submitError, setSubmitError] = useState(null)
  const submitPost = async (value) => {
    const endpointUrl= await process.env.NEXT_PUBLIC_BACKEND_ENDPOINT_URL
    const res = await fetch(`${endpointUrl}/post`, {
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
    }
  };
  

  return (
    <>
      <Modal isOpen={isOpen} onClose={onClose} size={{ base: 'lg', xs: 'xs' }}>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>投稿する</ModalHeader>
          <ModalCloseButton />
          <ModalBody>
            <form onSubmit={handleSubmit(submitPost)}>
              <FormControl isInvalid={!!errors.text}>
                <FormLabel>テキスト：</FormLabel>
                <Textarea
                  {...register('text', {
                    required: 'テキストを入力してください．',
                    maxLength:{
                      value: 200,
                      message: "投稿は200文字以下で入力してください．"
                    },
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
                <Button 
                  size="lg" 
                  colorScheme="green" 
                  type="submit" 
                  isLoading={isSubmitting}
                >
                  投稿する
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
