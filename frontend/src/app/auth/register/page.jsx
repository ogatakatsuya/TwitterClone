"use client";

import {
    Input,
    Button,
    FormErrorMessage,
    Heading,
    FormLabel,
    FormControl,
    Text,
    Link,
    Flex,
    Box,
    InputGroup,
    InputRightElement,
    Stack,
    useColorModeValue,
} from "@chakra-ui/react";

import { ViewIcon, ViewOffIcon } from "@chakra-ui/icons";

import { useForm } from "react-hook-form";
import { useState } from "react";
import { useRouter } from "next/navigation";

const Register = () => {
    const router = useRouter();
    const [showPassword, setShowPassword] = useState(false);
    const [submitError, setSubmitError] = useState();

    const {
        register,
        handleSubmit,
        formState: { errors, isSubmitting },
    } = useForm();

    const onSubmit = async (value) => {
        try {
            const endpointUrl = process.env.NEXT_PUBLIC_BACKEND_ENDPOINT_URL
            const res = await fetch(`${endpointUrl}/auth/register`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ user_name : value.userName, password : value.password }),
            })
    
        if (!res.ok) {
            const errorData = await res.json()
            setSubmitError(errorData.message || '何か問題が発生しました')
        } else {
            const data = await res.json()
            setSubmitError(null)
            router.push("/auth/login")
        }
        } catch (err) {
        setSubmitError('ネットワークエラーです。後で再試行してください。')
        console.error('ネットワークエラー:', err)
        }
    }

    return (
        <Flex
        minH={"100vh"}
        align={"center"}
        justify={"center"}
        bg={useColorModeValue("gray.50", "gray.800")}
        >
        <Box
            rounded={"lg"}
            bg={useColorModeValue("white", "gray.700")}
            boxShadow={"lg"}
            p={8}
            w={{ base: "90%", sm: "80%", md: "60%", lg: "50%", xl: "40%" }}
            maxW={"500px"}
        >
            <Heading fontSize={"2xl"} textAlign={"center"} py={4}>
            Get started
            </Heading>
            <Text fontSize={"1xl"} color={"gray.600"} textAlign={"center"}>
            Start setting up your account ✌️
            </Text>
            <form onSubmit={handleSubmit(onSubmit)}>
            <FormControl id="userName" isRequired isInvalid={!!errors.email} pt={6}>
                <FormLabel fontSize={"xl1"}>User name</FormLabel>
                <Input
                placeholder="John Doe"
                _placeholder={{ opacity: "0.3", color: "gray.500" }}
                {...register("userName", {
                    required: "名前は必須です。",
                })}
                />
                <FormErrorMessage>
                {errors.userName?.message}
                </FormErrorMessage>
            </FormControl>
            <FormControl
                id="password"
                isRequired
                isInvalid={!!errors.password}
                pt={6}
            >
                <FormLabel>Password</FormLabel>
                <InputGroup>
                <Input
                    placeholder="●●●●●●●●●"
                    _placeholder={{ opacity: "0.3", color: "gray.500" }}
                    {...register("password", {
                    required: "パスワードは必須です。",
                    minLength: {
                        value: 6,
                        message: "パスワードは6文字以上で入力してください。",
                    },
                    })}
                    type={showPassword ? "text" : "password"}
                />
                <InputRightElement h={"full"}>
                    <Button
                    variant={"ghost"}
                    onClick={() =>
                        setShowPassword((showPassword) => !showPassword)
                    }
                    >
                    {showPassword ? <ViewIcon /> : <ViewOffIcon />}
                    </Button>
                </InputRightElement>
                </InputGroup>
                <FormErrorMessage>
                {errors.password?.message}
                </FormErrorMessage>
            </FormControl>
            <Stack pt={6}>
                <Button
                loadingText="Submitting"
                bg={"black"}
                color={"white"}
                _hover={{
                    bg: "gray.700",
                }}
                type="submit"
                isLoading={isSubmitting}
                >
                Sign up
                </Button>
            </Stack>
            <Stack pt={6}>
                <Text align={"center"} color={"gray.500"}>
                Already a user?{" "}
                <Link color={"black.500"} href="/auth/login">
                    Login
                </Link>
                </Text>
            </Stack>
            </form>
        </Box>
        </Flex>
    );
};

export default Register;
