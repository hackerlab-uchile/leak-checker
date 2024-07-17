import {
  Dispatch,
  SetStateAction,
  useCallback,
  useEffect,
  useRef,
  useState,
} from "react";
import Script from "next/script";

export default function Turnstile({
  siteKey,
  onTokenChange,
  onErrorCallback,
  needReset,
  setNeedReset,
}: {
  siteKey: string;
  onTokenChange?: (token: string | null) => void;
  onErrorCallback?: () => void;
  needReset: boolean;
  setNeedReset: Dispatch<SetStateAction<boolean>>;
}) {
  const turnstileRef = useRef<HTMLDivElement | null>(null);
  const [turnstileLoaded, setTurnstileLoaded] = useState(false);
  const [currentWidgetId, setCurrentWidgetId] = useState<string>();

  useEffect(() => {
    if (needReset && currentWidgetId) {
      (window as any).turnstile.reset(currentWidgetId);
      setNeedReset(false);
    }
  }, [needReset, currentWidgetId]);

  useEffect(() => {
    const checkTurnstileLoaded = () => {
      onTokenChange?.(null);
      if (typeof (window as any).turnstile !== "undefined") {
        setTurnstileLoaded(true);
      } else {
        setTimeout(checkTurnstileLoaded, 100);
      }
    };

    checkTurnstileLoaded();
  }, []);

  useEffect(() => {
    if (turnstileLoaded && turnstileRef.current) {
      const widgetId = (window as any).turnstile.render(turnstileRef.current, {
        sitekey: siteKey, // Replace with your Turnstile site key
        callback: (token: string) => onTokenChange?.(token),
        "error-callback": () => {
          console.error("Turnstile challenge failed");
          onErrorCallback?.();
        },
        "expired-callback": () => {
          onTokenChange?.(null);
        },
      });
      setCurrentWidgetId(widgetId);
      return () => (window as any).turnstile.remove(widgetId);
    }
  }, [turnstileLoaded]);

  return (
    <>
      <Script
        src="https://challenges.cloudflare.com/turnstile/v0/api.js"
        async
        defer
      ></Script>
      <div ref={turnstileRef}></div>
    </>
  );
}
