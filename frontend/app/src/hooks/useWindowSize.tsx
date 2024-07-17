import { useState, useEffect } from "react";

export enum SizeType {
  XS = 0,
  SM = 640,
  MD = 768,
  LG = 1024,
}

interface WindowSize {
  width: number | undefined;
  height: number | undefined;
  sizeType: SizeType | undefined;
}

const useWindowSize = () => {
  const [windowSize, setWindowSize] = useState<WindowSize>({
    width: undefined,
    height: undefined,
    sizeType: undefined,
  });

  useEffect(() => {
    const handleResize = () => {
      const width = window.innerWidth;
      let sizeType: SizeType;
      if (width > SizeType.LG) {
        sizeType = SizeType.LG;
      } else if (width > SizeType.MD) {
        sizeType = SizeType.MD;
      } else if (width > SizeType.SM) {
        sizeType = SizeType.SM;
      } else {
        sizeType = SizeType.XS;
      }
      console.log("Size: ", sizeType);

      setWindowSize({
        width: window.innerWidth,
        height: window.innerHeight,
        sizeType: sizeType,
      });
    };

    window.addEventListener("resize", handleResize);

    handleResize();

    return () => window.removeEventListener("resize", handleResize);
  }, []);

  return windowSize;
};

export default useWindowSize;
