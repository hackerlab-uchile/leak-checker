import React from "react";

import { cn } from "@/lib/utils";

interface CircleNumberProps extends React.HTMLAttributes<HTMLParagraphElement> {
  aNumber: number;
}

const CircleNumber = React.forwardRef<HTMLParagraphElement, CircleNumberProps>(
  ({ className, aNumber, ...props }, ref) => (
    <p
      ref={ref}
      className={cn(
        "w-[50px] leading-[50px] rounded-full text-center",
        className
      )}
      {...props}
    >
      {aNumber}
    </p>
  )
);
CircleNumber.displayName = "CircleNumber";

export default CircleNumber;
