"use client"

import { Heading } from "@chakra-ui/react";
import ToLoginButton from './_components/ToLoginButton';
import ToRegisterButton from './_components/ToRegisterButton';

import { useEffect, useState } from "react";

export default function Home() {
  const [data, setMessage] = useState("");
  useEffect(() => { //接続確認用
    fetch("http://localhost:8000/hello")
      .then((res) => res.json())
      .then((data) => setMessage(data));
  }, []);
  return (
    <>
      <Heading>{data}</Heading> 
      <ToLoginButton />
      <ToRegisterButton />
    </>
  );
}
