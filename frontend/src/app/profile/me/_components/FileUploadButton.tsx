import React, { useRef } from 'react';
import { Button } from '@chakra-ui/react';

const FileUploadButton = () => {
  const fileInputRef = useRef(null);

  const handleButtonClick = () => {
    fileInputRef.current.click();
  };

  const handleFileChange = async (event) => {
    const file = event.target.files[0];
    if (file) {
      console.log('Selected file:', file);

      // FormDataを作成し、ファイルを追加
      const formData = new FormData();
      formData.append('file', file);

      try {
        // バックエンドのエンドポイントURL
        const endpointUrl = process.env.NEXT_PUBLIC_BACKEND_ENDPOINT_URL;

        // POSTリクエストを送信
        const res = await fetch(`${endpointUrl}/profile/icon`, {
          method: 'POST',
          body: formData,
          credentials: 'include' // クッキーを送信する場合に必要
        });

        if (!res.ok) {
          const data = await res.json();
          console.error('Upload failed:', data);
          // エラー処理を行う
        } else {
          const data = await res.json();
          console.log('Upload successful:', data);
          // 成功時の処理を行う
        }
      } catch (error) {
        console.error('Error uploading file:', error);
        // エラー処理を行う
      }
    }
  };

  return (
    <>
      <Button bgColor="green.200" onClick={handleButtonClick}>
        Add Icon Image
      </Button>
      <input
        type="file"
        ref={fileInputRef}
        style={{ display: 'none' }}
        onChange={handleFileChange}
      />
    </>
  );
};

export default FileUploadButton;
