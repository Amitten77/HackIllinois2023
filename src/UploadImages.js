import React, { useState, useEffect } from 'react';
import history from './history';

export default function UploadImages() {
    const [images, setImages] = useState([]);
    const [imageURLs, setImageURLs] = useState([]);

    useEffect(() => {
        if (images.length < 1) return;
        const newImageUrls = [];
        images.forEach(image => newImageUrls.push(URL.createObjectURL(image)));
        setImageURLs(newImageUrls);
    }, [images]);

    function onImageChange(e) {
        setImages([...e.target.files]);
    }

    return (
        <div className="center">
            <label className="file">
                <input id="file" type="file" multiple accept="image/*" onChange={() => history.push('/Results')} />
                { imageURLs.map(imageSrc => <img src={imageSrc} />) }

                <span className="file-custom"></span>
            </label>
        </div>
    );
    /*
    return (
        <div className="center">
            <label className="file">
                <input id="file" type="file" multiple accept="image/*"  />
                { imageURLs.map(imageSrc => <img src={imageSrc} onChange={onImageChange}/>)}
                <span className="file-custom"></span>
            </label>
        </div>
    );
    */
}