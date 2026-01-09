import { useState, useEffect, useCallback } from 'react';

type CarouselProps = {
    images: string[],
    width?: number,
    height?: number,
}

export const Carousel = ({ images, width = 600, height = 600 }: CarouselProps) => {
    const [index, setIndex] = useState<number>(0);

    const hasImages = images && images.length;

    const prev = useCallback((): void => {
        setIndex(i=>(i-1 + images.length)%images.length)
    }, [images.length]);
    const next = useCallback((): void => {
        setIndex(i=>((i+1)%images.length))
    }, [images.length]);

    useEffect(()=>{
        if (!hasImages)
            return;

        const onKeyDown = (e:KeyboardEvent) => {
            if (e.key === "ArrowLeft" || e.key === "a")
                prev();
            if (e.key === "ArrowRight" || e.key === "d")
                next();
        };

        window.addEventListener("keydown", onKeyDown);
        return window.removeEventListener("keydown", onKeyDown);
    }, [hasImages, images.length, next, prev]);
    return (
        <div style={{width}}>
            <div style={{
                display:'flex',
                justifyContent:'center',
                position: "relative",
                width: "100%",
                height,
                overflow: "hidden",
                borderRadius: 12,
                border: "1px solid #ddd",
                background: "#f6f6f6",
            }}>
                <img 
                    src={images[index]} 
                    alt={images[(index+1)%images.length]} 
                    style={{ width: "100%", height: "100%", objectFit: "cover", display: "block" }}
                />
            </div>
        <button
            type="button"
            onClick={prev}
            aria-label="Previous image"
            style={{
                position: "absolute",
                left: 10,
                top: "50%",
                transform: "translateY(-50%)",
                borderRadius: 999,
                border: "1px solid #ccc",
                background: "white",
                padding: "8px 10px",
                cursor: "pointer",
            }}
        >
          ◀
        </button>
        <button
            type="button"
            onClick={next}
            aria-label="Next image"
            style={{
                position: "absolute",
                right: 10,
                top: "50%",
                transform: "translateY(-50%)",
                borderRadius: 999,
                border: "1px solid #ccc",
                background: "white",
                padding: "8px 10px",
                cursor: "pointer",
            }}
        >
          ▶
        </button>
        </div>
    )
}