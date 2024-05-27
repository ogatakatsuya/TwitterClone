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
import { useForm, SubmitHandler } from "react-hook-form";
import { useRouter } from "next/navigation";

const Login = () => {
    const router = useRouter();

    const {
        register,
        handleSubmit,
        formState: { errors, isSubmitting },
    } = useForm();

    const onSubmit = (data) => {
        console.log(data);
        router.push("/")
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
            <FormControl id="email" isRequired isInvalid={!!errors.email} pt={6}>
                <FormLabel fontSize={"xl1"}>Email address</FormLabel>
                <Input
                placeholder="sample@email.com"
                _placeholder={{ opacity: "0.3", color: "gray.500" }}
                {...register("email", {
                    required: "メールアドレスは必須です。",
                    pattern: {
                    value:
                        /^[a-zA-Z0-9_.+-]+@([a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9]*\.)+[a-zA-Z]{2,}$/,
                    message: "不適切なメールアドレスです。",
                    },
                })}
                />
                <FormErrorMessage>
                {errors.email && errors.email.message}
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
                {errors.password && errors.password.message}
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
        </Flex>
    );
};

export default Login;
