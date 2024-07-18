'use client'

import { useState, useRef } from 'react'
import { useForm, SubmitHandler } from 'react-hook-form'
import toast, { Toaster } from 'react-hot-toast'
import {
  Button,
  FormErrorMessage,
  FormLabel,
  Heading,
  FormControl,
  Text,
  Textarea,
  Box,
  Input,
  Flex,
  Image,
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalFooter,
  ModalBody,
  ModalCloseButton,
} from '@chakra-ui/react'

export default function PostModal({ isOpen, onOpen, onClose, setPost }) {
  const {
    register,
    handleSubmit,
    setValue,
    watch,
    formState: { errors, isSubmitting },
  } = useForm()

  const [submitError, setSubmitError] = useState(null);
  const inputRef = useRef(null);
  const previewUrl = watch('preview_url');
  const notify = () => toast.success('Successfully posted!');

  const onFileInputChange = (event) => {
    const { files } = event.target;
    if (files && files[0]) {
      setValue('preview_url', URL.createObjectURL(files[0])); // 動いた!!
    }
  };

  const submitPost = async (values) => {
    const endpointUrl = process.env.NEXT_PUBLIC_BACKEND_ENDPOINT_URL;
    const formData = new FormData();
    formData.append('text', values.text);
    
    if (inputRef.current && inputRef.current.files[0]) {
      formData.append('file', inputRef.current.files[0]);
    }

    const res = await fetch(`${endpointUrl}/post`, {
      method: "POST",
      credentials: "include",
      body: formData,
    });

    if (!res.ok) {
      const data = await res.json();
      setSubmitError(data.detail);
    } else {
      onClose();
      const data = await res.json();
      setPost((prevPosts) => [data, ...prevPosts]);
      notify();
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
                    maxLength: {
                      value: 200,
                      message: "投稿は200文字以下で入力してください．"
                    },
                  })}
                />
                <FormErrorMessage>{errors.text?.message}</FormErrorMessage>
                <Input
                  ref={inputRef}
                  name="preview_url"
                  type="file"
                  accept="image/*"
                  onChange={onFileInputChange}
                />
                {previewUrl && (
                  <Box mt={4}>
                      <Image src={previewUrl} alt="Preview" width="100%" />
                  </Box>
                )}
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
          <ModalFooter />
        </ModalContent>
      </Modal>
      <Toaster />
    </>
  )
}
