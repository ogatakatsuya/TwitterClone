"use client";

import { useEffect, useState } from "react"
import { 
    Card, 
    CardHeader, 
    CardBody, 
    CardFooter ,
    Stack,
    Text,
    StackDivider,
    Box,
    Heading,
    Avatar,
    Flex,
    IconButton,
    useDisclosure,
} from '@chakra-ui/react'
import CommentModal from "./CommentModal"
import { BiLike } from "react-icons/bi";
import { BiSolidLike } from "react-icons/bi";
import { FaRegCommentDots } from "react-icons/fa";

const PostIndex = () => {
    const [post, setPost] = useState([]);
    const [pushed, setPushed] = useState(false);
    const { isOpen, onOpen, onClose } = useDisclosure()
    const fetchPost = async () => {
        try {
            const res = await fetch("http://localhost:8000/post", {
                method: "GET",
            });
            if (res.ok) {
                const data = await res.json();
                setPost(data);
                console.log(data); // データをログに出力する
            } else {
                console.error("Error fetching posts:", res.statusText);
            }
        } catch (error) {
            console.error("Error fetching posts:", error);
        }
    }
    
    useEffect(() => {
        fetchPost();
    },[])

    const handleLike = () => {
        setPushed((prev) => !prev)
    };

    return (
        <>
        <Stack divider={<StackDivider />} spacing='4'>
            {post.map((item) => (
                <Card width="500px">
                    <CardBody>
                        <Flex alignItems="center">
                            <Avatar />
                            <Box ml={3}>
                                <Text fontSize='md'>
                                    John Doe
                                </Text>
                                <Text fontSize='xs'>
                                    {item.created_at}
                                </Text>
                            </Box>
                        </Flex>
                        <Box key={item.id}>
                            <Text mt='4' fontSize='md'>
                                {item.text}
                            </Text>
                        </Box>
                        <Flex mt={2}>
                            <IconButton 
                                icon={pushed ? <BiSolidLike /> : <BiLike />} 
                                onClick={() => handleLike()}
                                aria-label="Like button"
                                mr="4"
                                size="sm"
                            />
                            <IconButton 
                                icon={<FaRegCommentDots/>}
                                aria-label="Comment Button"
                                onClick={onOpen}
                                size="sm"
                            />
                        </Flex>
                    </CardBody>
                    {/* <CardFooter>
                        <Flex>
                            <IconButton 
                                icon={pushed ? <BiSolidLike /> : <BiLike />} 
                                onClick={() => handleLike()}
                                aria-label="Like button"
                                mr="4"
                                size="sm"
                            />
                            <IconButton 
                                icon={<FaRegCommentDots/>}
                                aria-label="Comment Button"
                                onClick={onOpen}
                                size="sm"
                            />
                        </Flex>
                    </CardFooter> */}
                </Card>
            ))}
        </Stack>
        <CommentModal onClose={onClose} onOpen={onOpen} isOpen={isOpen}/>
        </>
    )
}

export default PostIndex;
