import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

interface SkeletonProps {
  className?: string;
}

export function Skeleton({ className }: SkeletonProps) {
  return (
    <div
      className={twMerge(
        clsx("animate-pulse rounded-md bg-slate-800/50", className)
      )}
    />
  );
}