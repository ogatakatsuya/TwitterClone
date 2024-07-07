"use client"

import { Heading } from "@chakra-ui/react";
import ToLoginButton from './_components/ToLoginButton';
import ToRegisterButton from './_components/ToRegisterButton';

import { useEffect, useState } from "react";

export default function Home() {
  const [data, setMessage] = useState("");
  useEffect(() => { //接続確認用
    const endpoitUrl = process.env.NEXT_PUBLIC_BACKEND_ENDPOINT_URL;
    fetch(`${endpoitUrl}/hello`)
      .then((res) => res.json())
      .then((data) => setMessage(data));
  }, []);
  return (
    <>
      <h1>hello</h1>
      <Heading>{data}</Heading> 
      <ToLoginButton />
      <ToRegisterButton />
    </>
  );
}
