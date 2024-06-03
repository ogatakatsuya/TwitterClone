"use client";
import { Heading } from "@chakra-ui/react"
import { useEffect, useState } from "react";
import ToLoginButton from './_components/ToLoginButton'
import ToRegisterButton from './_components/ToRegisterButton'

export default function Home() {
  return (
    <>
    <Heading>Hello</Heading>
    <ToLoginButton />
    <ToRegisterButton />
    </>
  );
}
