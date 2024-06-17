"use client";

import { Button } from "@chakra-ui/react";
import { useState, useEffect } from "react";

const FollowButton = () => {
    const [ following, setFollowing ] = useState(false);
    const clickHandler = () => {
        setFollowing(!following)
    }
    return (
        <> 
            {following ? (
                <Button onClick={clickHandler}>
                    Following
                </Button>
            ):
                <Button onClick={clickHandler}>
                    Follow
                </Button>
            }
        </>
    )
}

export default FollowButton;