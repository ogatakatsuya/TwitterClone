"use client";

import { useState, useEffect } from 'react'
import { 
    Card,
    CardBody,
    Text,
    Box,
    Avatar,
    Flex,
    IconButton,
    useDisclosure,
} from '@chakra-ui/react'
import { BiLike } from "react-icons/bi";
import { BiSolidLike } from "react-icons/bi";
import { FaRegCommentDots } from "react-icons/fa";
import CommentModal from './ReplyModal';

const Post = ({ post_id }) => {
    const [ pushed, setPushed ] = useState(false);
    const [ post, setPost ] = useState("");
    const { isOpen, onOpen, onClose } = useDisclosure()
    
    const fetchPost = async () => {
        const endpointUrl= process.env.NEXT_PUBLIC_BACKEND_ENDPOINT_URL
        const res = await fetch(`${endpointUrl}/post/${post_id}`)
        if(res.ok){
            const data = await res.json();
            console.log(data)
            setPost(data);
        }
    }

    const handleLike = () => {
        setPushed((prev) => !prev)
    };

    useEffect(() => {
        fetchPost();
    }, [])
    return (
        <>
            <Card width="500px">
                <CardBody>
                    <Flex alignItems="center">
                        <Avatar />
                        <Box ml={3}>
                            <Text fontSize='md'>
                                John Doe
                            </Text>
                            <Text fontSize='xs'>
                                {post.created_at}
                            </Text>
                        </Box>
                    </Flex>
                    <Box>
                        <Text mt='4' fontSize='md'>
                            {post.text}
                        </Text>
                    </Box>
                    <Flex 
                        justifyContent="flex-end" 
                        alignItems="flex-end"
                        style={{ position: 'absolute', bottom: '10px', right: '10px' }}
                    >
                        <IconButton 
                            icon={pushed ? <BiSolidLike /> : <BiLike />} 
                            onClick={() => handleLike()}
                            aria-label="Like button"
                            mr="4"
                            size="sm"
                        />
                        <IconButton 
                            icon={<FaRegCommentDots />}
                            aria-label="Comment Button"
                            onClick={onOpen}
                            size="sm"
                        />
                    </Flex>
                </CardBody>
            </Card>
            <CommentModal onClose={onClose} isOpen={isOpen} post_id={post_id}/>
        </>
    )
}

export default Post;