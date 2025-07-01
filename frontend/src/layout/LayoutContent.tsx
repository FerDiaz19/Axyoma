import React from "react";

interface LayoutContentProps {
    title: string;
    children: React.ReactNode;
}

const LayoutContent: React.FC<LayoutContentProps> = ({ title, children }) => {
    return (
        <div className="flex flex-col gap-4 bg-gray-50 p-4 rounded shadow-md">
            <div>{title}</div>
            {children}
        </div>
    );
}

export default LayoutContent;