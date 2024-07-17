"use client";

import {
    Input,
    Button,
    FormErrorMessage,
    FormLabel,
    Heading,
    FormControl,
    Text,
    Link,
    Box,
    Flex,
    InputGroup,
    Stack,
    useColorModeValue,
} from "@chakra-ui/react";
import toast, { Toaster } from 'react-hot-toast';
import { useForm, SubmitHandler } from "react-hook-form";
import { useRouter } from "next/navigation";
import { useState } from "react";

const Login = () => {
    const router = useRouter();
    const [submitError, setSubmitError] = useState();
    const notify = () => toast.error("ユーザー名かパスワードが間違っています。")

    const {
        register,
        handleSubmit,
        formState: { errors, isSubmitting },
    } = useForm();

    const onSubmit = async (value) => {
        try {
            const endpointUrl= process.env.NEXT_PUBLIC_BACKEND_ENDPOINT_URL
            const res = await fetch(`${endpointUrl}/auth/login`, {
                method: 'POST',
                credentials: "include",
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams({
                    'username': value.userName,
                    'password': value.password,
                }),
            });
    
            if (!res.ok) {
                const errorData = await res.json();
                notify();
                setSubmitError(errorData.detail || '何か問題が発生しました');
            } else {
                const data = await res.json();
                console.log(data);
                setSubmitError(null);
                router.push("/home");
            }
        } catch (err) {
            setSubmitError('ネットワークエラーです。後で再試行してください。');
            console.error('ネットワークエラー:', err);
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
            Login
            </Heading>
            <Text fontSize={"1xl"} color={"gray.600"} textAlign={"center"}>
            Welcome back 🥰{" "}
            </Text>
            <form onSubmit={handleSubmit(onSubmit)}>
            <FormControl id="userName" isRequired isInvalid={!!errors.userName} pt={6}>
                <FormLabel fontSize={"xl1"}>User name</FormLabel>
                <Input
                placeholder="John Doe"
                _placeholder={{ opacity: "0.3", color: "gray.500" }}
                {...register("userName", {
                    required: "メールアドレスは必須です。",
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
                    type={"password"}
                />
                </InputGroup>
                <FormErrorMessage>
                {errors.password?.message}
                </FormErrorMessage>
            </FormControl>
            <Stack pt={6}>
                <Button
                loadingText="Logging in..."
                bg={"black"}
                color={"white"}
                _hover={{
                    bg: "gray.700",
                }}
                type="submit"
                isLoading={isSubmitting}
                >
                Login
                </Button>
            </Stack>
            <Stack pt={6}>
                <Text align={"center"} color={"gray.500"}>
                Don't have an account yet?{" "}
                <Link color={"black.500"} href="/auth/register">
                    Sign up here
                </Link>
                </Text>
            </Stack>
            </form>
        </Box>
        <Toaster/>
        </Flex>
    );
};

export default Login;
